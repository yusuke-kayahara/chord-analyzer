#!/usr/bin/env python3
"""
Extended test for context-aware borrowed key analysis with multiple borrowed chords
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import (
    extract_chords, detect_non_diatonic_notes, find_borrowed_sources,
    calculate_key_confidence, get_chord_components
)

def test_multiple_borrowed_chords():
    print("=== Extended Context-Aware Test ===\n")
    
    # Test progression with multiple borrowed chords
    test_input = "[C][Am][F][Fm][C][G][AbM7][G]"
    main_key = "C Major"
    
    print(f"Test progression: {test_input}")
    print(f"Main key: {main_key}")
    print()
    
    chords = extract_chords(test_input)
    print(f"Extracted chords: {chords}")
    
    non_diatonic_chords = detect_non_diatonic_notes(chords, main_key)
    print(f"Non-diatonic chords: {[chord['chord'] for chord in non_diatonic_chords]}")
    
    if non_diatonic_chords:
        borrowed_chords = find_borrowed_sources(non_diatonic_chords, main_key, chords)
        
        for borrowed in borrowed_chords:
            print(f"\n--- Analyzing {borrowed.chord} ---")
            chord_index = chords.index(borrowed.chord)
            
            print(f"Position in progression: {chord_index + 1} of {len(chords)}")
            print(f"Context analysis:")
            
            context_info = []
            if chord_index > 0:
                prev = chords[chord_index - 1]
                context_info.append(f"Previous: {prev}")
            if chord_index < len(chords) - 1:
                next_chord = chords[chord_index + 1]
                context_info.append(f"Next: {next_chord}")
            
            print(f"  {' | '.join(context_info)}")
            
            print("Top 3 source candidates (context-enhanced):")
            for i, candidate in enumerate(borrowed.source_candidates[:3]):
                print(f"  {i+1}. {candidate.key}")
                print(f"     Relationship: {candidate.relationship}")
                print(f"     Confidence: {candidate.confidence:.3f}")

if __name__ == "__main__":
    test_multiple_borrowed_chords()