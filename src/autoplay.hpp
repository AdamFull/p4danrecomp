#pragma once

// An automatic player, for testing a song from start to end (P4D_AUTOPLAY=<chart>[,<offset ms>]): it presses each
// note's button at the note's time by the game's own dance clock, as the game reads the controller. The chart is
// the song's note sequence file (dance/mns/mnsNNN_D.bin from data.cpk, extracted with scripts/mns_chart.py); the
// offset moves every press later (or earlier, negative) to find where the judgement windows are.
//
// What it relies on (the update 01.01's executable): the dance process function at 0x8101EA62, called through a
// pointer once a frame with its process, whose third word points to the dance state; the dance time (seconds, a
// float) at +0x1DC there. A chart's notes are 8 bytes from 0x24: the position (the measure in the upper half, the
// beat in the lower, bit 15 an eighth) and the lane (0 down, 1 cross, 2 left, 3 circle, 4 up, 5 triangle in the low
// byte; 8 a scratch). These were read from the code and checked against the notes on the screen.

namespace psvrecore::runtime {
class Runtime;
}

namespace p4d {

// Installs the player when P4D_AUTOPLAY is set (a debugging aid: nothing changes without it).
void prepare_autoplay(psvrecore::runtime::Runtime& rt);

}  // namespace p4d
