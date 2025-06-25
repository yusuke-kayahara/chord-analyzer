#!/usr/bin/env python3
"""
Test script for context-aware borrowed key analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from main.py
from main import (
    extract_chords, detect_non_diatonic_notes, find_borrowed_sources,
    calculate_key_confidence, get_chord_components
)

def test_context_aware_analysis():
    print("=== Context-Aware Borrowed Key Analysis Test ===\n")
    
    # Test chord progression with clear context
    test_input = "[CM7][Am7][Fm][G7]"
    main_key = "C Major"
    
    print(f"Test progression: {test_input}")
    print(f"Main key: {main_key}")
    print()
    
    # Extract chords
    chords = extract_chords(test_input)
    print(f"Extracted chords: {chords}")
    
    # Detect non-diatonic chords
    non_diatonic_chords = detect_non_diatonic_notes(chords, main_key)
    print(f"Non-diatonic chords: {[chord['chord'] for chord in non_diatonic_chords]}")
    
    if non_diatonic_chords:
        print("\n=== Testing Context-Aware Analysis ===")
        
        # Test borrowed chord analysis with context
        borrowed_chords = find_borrowed_sources(non_diatonic_chords, main_key, chords)
        
        for borrowed in borrowed_chords:
            print(f"\nChord: {borrowed.chord}")
            print(f"Non-diatonic notes: {borrowed.non_diatonic_notes}")
            
            # Get context for this chord
            chord_index = chords.index(borrowed.chord)
            context_notes = []
            
            # Previous chord context
            if chord_index > 0:
                prev_chord = chords[chord_index - 1]
                prev_notes = get_chord_components(prev_chord)
                context_notes.extend(prev_notes)
                print(f"Previous chord ({prev_chord}): {prev_notes}")
            
            # Next chord context
            if chord_index < len(chords) - 1:
                next_chord = chords[chord_index + 1]
                next_notes = get_chord_components(next_chord)
                context_notes.extend(next_notes)
                print(f"Next chord ({next_chord}): {next_notes}")
            
            context_notes = list(set(context_notes))
            print(f"Combined context notes: {context_notes}")
            
            print("Source candidates (with context):")
            for i, candidate in enumerate(borrowed.source_candidates[:3]):
                # Test confidence with and without context
                chord_notes = get_chord_components(borrowed.chord)
                confidence_without_context = calculate_key_confidence(chord_notes, candidate.key)
                confidence_with_context = calculate_key_confidence(chord_notes, candidate.key, context_notes)
                
                print(f"  {i+1}. {candidate.key} ({candidate.relationship})")
                print(f"     Without context: {confidence_without_context:.3f}")
                print(f"     With context: {confidence_with_context:.3f}")
                print(f"     Context boost: {confidence_with_context - confidence_without_context:.3f}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_context_aware_analysis()