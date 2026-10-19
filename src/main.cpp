// Persona 4: Dancing All Night as a native program: the game described for psvrecore's frontend, which reads the
// settings and the command line, opens the window and the audio device, and runs the recompiled game.
//
// The game's code is generated from its executable once the packages are decrypted (milestone M7), and only for the
// versions listed below: an executable whose SHA-256 is not listed is refused, never run. Until then the list is
// empty and the program stops at that check.

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
    const char* sha256;  // eboot.bin's, in lower-case hex
};

// (none yet: the executable is known once the packages are decrypted)
constexpr std::span<const Version> kVersions{};

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
    return failure(nx::format("{} is not a version this build supports (SHA-256 {}).{}", eboot, digest,
                              kVersions.empty() ? " No version is supported yet: the game's code has not been "
                                                  "generated (milestone M7)."
                                                : ""));
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
