// Persona 4: Dancing All Night as a native program: the game described for psvrecore's frontend, which reads the
// settings and the command line, opens the window and the audio device, and runs the recompiled game.
//
// The game's code is generated from its executable (the update's, as a plaintext ELF) and only runs the versions
// listed below: an executable whose SHA-256 is not listed is refused, never run.

#include <SDL3/SDL_main.h>

#include <span>

#include "psvrecore/frontend/frontend.hpp"
#include "psvrecore/io/file.hpp"
#include "core/foundation/core/sha256.h"
#include "core/foundation/strings/format.h"

namespace {

using namespace psvrecore;

// A version the code was generated from.
struct Version {
    const char* name;    // ("EU 01.01")
    const char* sha256;  // eboot.bin's (the plaintext ELF), in lower-case hex
};

// (the update's executable: the base game's 01.00 alone is not supported)
constexpr Version kVersionList[] = {
    {"EU 01.01", "aa6e1260561393262695063edb4b8bdf9095aa727d248a7f3d9b83851f4d2261"},
};
constexpr std::span<const Version> kVersions{kVersionList};

// The recompiled modules (none yet).
constexpr std::span<const PsvModuleCode* const> kCode{};

nx::string hex(std::span<const u8> bytes) {
    nx::string s;
    for (u8 b : bytes) s += nx::format("{:02x}", b);
    return s;
}

Result<void> check_version(const nx::string& game_folder) {
    const nx::string eboot = game_folder + "/eboot.bin";
    auto bytes = io::read_file(nx::fs::path_view(eboot));
    if (!bytes) return failure(nx::format("{}: {}", eboot, bytes.error().message));
    const nx::string digest = hex(nx::sha256(std::span<const u8>(bytes->data(), bytes->size())));
    for (const Version& v : kVersions)
        if (digest == v.sha256) return {};
    return failure(nx::format("{} is not a version this build supports (SHA-256 {}). Supported: the update 01.01 "
                              "(EU, PCSB00867) as a plaintext ELF.",
                              eboot, digest));
}

}  // namespace

int main(int argc, char** argv) {
    frontend::Game game;
    game.name = "p4danrecomp";
    game.title = "Persona 4: Dancing All Night";
    game.title_id = "PCSB00867";
    game.code = kCode;
    game.check = check_version;
    return frontend::run(game, argc, argv);
}
