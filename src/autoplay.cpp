#include "autoplay.hpp"

#include <algorithm>
#include <atomic>
#include <cstdlib>
#include <cstring>

#include "psvrecore/io/file.hpp"
#include "psvrecore/log.hpp"
#include "psvrecore/recomp/support.hpp"
#include "psvrecore/runtime/runtime.hpp"
#include "core/foundation/strings/format.h"

namespace p4d {

namespace {

using namespace psvrecore;

constexpr u32 kDanceProcess = 0x8101EA63;  // (Thumb code: the registry keeps bit 0 set)
constexpr u32 kDanceTime = 0x1DC;
constexpr u32 kScratch = 8;
// (the lanes' buttons: SCE_CTRL_DOWN, CROSS, LEFT, CIRCLE, UP, TRIANGLE)
constexpr u32 kButtons[6] = {1u << 6, 1u << 14, 1u << 7, 1u << 13, 1u << 4, 1u << 12};

struct Lane {
    nx::vector<f32> times;  // (the notes' times, in order)
    usize next = 0;
    bool down = false;
    u32 reads = 0;   // (reads since it went down, or up)
    u32 frame = 0;   // (the dance frame it went down, or up, in)
};

struct Player {
    runtime::Runtime* rt = nullptr;
    PsvFunction dance_process = nullptr;
    f32 offset = 0;
    Lane lanes[7];  // (six buttons, then the scratches)
    // (written by the dance process each frame, read by the filter on the same thread: atomics for the order)
    std::atomic<u32> time_bits{0};
    std::atomic<u32> step_bits{0};  // (how far the dance time went in its last frame)
    std::atomic<u32> frames{0};
    std::atomic<u64> updated_ns{0};
    f32 previous_time = 0;  // (the dance process's, at its previous frame)
    f32 last_time = 0;
    u32 pressed = 0, late = 0;
};

Player g_player;

void dance_process(PsvContext* ctx, uint32_t ret) {
    const u32 process = ctx->r[0];
    g_player.dance_process(ctx, ret);
    runtime::GuestMemory& m = g_player.rt->memory();
    if (!m.valid(process + 8, 4)) return;
    const u32 dance = psv_ld32(process + 8);
    if (!m.valid(dance + kDanceTime, 4)) return;
    const u32 bits = psv_ld32(dance + kDanceTime);
    f32 t;
    std::memcpy(&t, &bits, sizeof t);
    const f32 step = t - g_player.previous_time;
    g_player.previous_time = t;
    u32 step_bits;
    std::memcpy(&step_bits, &step, sizeof step);
    g_player.time_bits.store(bits, std::memory_order_relaxed);
    g_player.step_bits.store(step_bits, std::memory_order_relaxed);
    g_player.frames.fetch_add(1, std::memory_order_relaxed);
    g_player.updated_ns.store(g_player.rt->kernel().clock_ns(), std::memory_order_release);
}

void play(runtime::PadState& s, u64, void*) {
    Player& p = g_player;
    const u64 updated = p.updated_ns.load(std::memory_order_acquire);
    const u64 now = p.rt->kernel().clock_ns();
    if (!updated || now - updated > 300'000'000ull) return;  // (no dance going on)
    const u32 bits = p.time_bits.load(std::memory_order_relaxed), step_bits = p.step_bits.load(std::memory_order_relaxed);
    const u32 frame = p.frames.load(std::memory_order_relaxed);
    f32 t, step;
    std::memcpy(&t, &bits, sizeof t);
    std::memcpy(&step, &step_bits, sizeof step);
    if (t <= 0) return;
    // The time the frame about to run will judge this read's presses at: the game's clock moves in steps (its
    // sound engine's ticks, the frames), so the last step says more than the time passed since.
    step = nx::clamp(step, 0.02f, 0.15f);
    t += step;
    if (t + 1.0f < p.last_time) {  // (a new dance: from its first note again)
        for (Lane& l : p.lanes) l.next = 0, l.down = false;
        nx::logi(logs::frontend, "autoplay: a new dance; {} pressed, {} too late", p.pressed, p.late);
        p.pressed = p.late = 0;
    }
    p.last_time = t;
    for (u32 i = 0; i < 7; ++i) {
        Lane& l = p.lanes[i];
        ++l.reads;
        // (down for a dance frame and two reads at least, then up as long before the next press)
        if (l.down && l.reads >= 2 && frame > l.frame) l.down = false, l.reads = 0, l.frame = frame;
        while (l.next < l.times.size() && t > l.times[l.next] + p.offset + 0.15f) ++l.next, ++p.late;
        // (pressed in the frame whose time is the nearest to the note's)
        if (!l.down && l.reads >= 2 && frame > l.frame && l.next < l.times.size() &&
            t + step / 2 >= l.times[l.next] + p.offset) {
            l.down = true, l.reads = 0, l.frame = frame;
            nx::logd(logs::frontend, "autoplay: lane {} note at {:.3f} s pressed at {:.3f} s", i, l.times[l.next], t);
            ++l.next, ++p.pressed;
        }
        if (!l.down) continue;
        if (i < 6) s.buttons |= kButtons[i];
        else s.lx = s.rx = 0xFF;  // (a scratch: the sticks to one side)
    }
}

}  // namespace

void prepare_autoplay(runtime::Runtime& rt) {
    const char* spec = std::getenv("P4D_AUTOPLAY");
    if (!spec || !*spec) return;
    nx::string path(spec);
    if (const usize comma = path.view().find(','); comma != nx::string_view::npos) {
        g_player.offset = static_cast<f32>(std::atof(path.c_str() + comma + 1)) / 1000.0f;
        path = nx::string(path.view().substr(0, comma));
    }
    auto bytes = io::read_file(nx::fs::path_view(path));
    if (!bytes || bytes->size() < 36 || std::memcmp(bytes->data(), "MNS", 4) != 0) {
        nx::logw(logs::frontend, "autoplay: {} is not a note sequence (MNS)", path);
        return;
    }
    const u8* d = bytes->data();
    f32 bpm;
    u32 count;
    std::memcpy(&bpm, d + 16, 4);
    // (the header's count leaves out some notes at the end: the notes fill the rest of the file)
    count = static_cast<u32>((bytes->size() - 36) / 8);
    if (bpm <= 0) {
        nx::logw(logs::frontend, "autoplay: {}: {} notes at {} beats a minute do not fit", path, count, bpm);
        return;
    }
    u32 taps = 0, scratches = 0;
    for (u32 i = 0; i < count; ++i) {
        u32 pos, lane;
        std::memcpy(&pos, d + 36 + 8 * i, 4);
        std::memcpy(&lane, d + 40 + 8 * i, 4);
        const f32 beat = static_cast<f32>((pos >> 16) * 4 + (pos & 0x7FFF)) + ((pos & 0x8000) ? 0.5f : 0.0f);
        const f32 time = beat * 60.0f / bpm;
        const u32 low = lane & 0xFF;
        if (low < 6) g_player.lanes[low].times.push_back(time), ++taps;
        else if (low == kScratch) g_player.lanes[6].times.push_back(time), ++scratches;
    }
    for (Lane& l : g_player.lanes) std::sort(l.times.begin(), l.times.end());
    g_player.rt = &rt;
    g_player.dance_process = recomp::override_function(kDanceProcess, dance_process);
    if (!g_player.dance_process) {
        nx::logw(logs::frontend, "autoplay: no dance process at {:08x} (another version?)", kDanceProcess);
        return;
    }
    rt.input().set_pad_filter(play, nullptr);
    nx::logi(logs::frontend, "autoplay: {} ({} beats a minute): {} notes, {} scratches; presses {:+.0f} ms from the notes",
             path, bpm, taps, scratches, g_player.offset * 1000.0f);
}

}  // namespace p4d
