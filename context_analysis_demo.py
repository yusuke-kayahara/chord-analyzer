#!/usr/bin/env python3
"""
Demonstration of context-aware borrowed key analysis enhancement
Shows the improvement in borrowed key confidence calculation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import (
    extract_chords, detect_non_diatonic_notes, find_borrowed_sources,
    calculate_key_confidence, get_chord_components, get_diatonic_notes
)

def demonstrate_context_enhancement():
    print("=" * 60)
    print("CONTEXT-AWARE BORROWED KEY ANALYSIS DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Test cases demonstrating context improvement
    test_cases = [
        {
            "name": "Jazz ii-V-I with borrowed iv",
            "progression": "[Dm7][G7][CM7][Fm][C]",
            "key": "C Major",
            "focus_chord": "Fm",
            "expected_improvement": "Fm should show higher confidence for C Minor due to resolution to C"
        },
        {
            "name": "Modal interchange progression",
            "progression": "[C][F][AbM7][G][C]",
            "key": "C Major",
            "focus_chord": "AbM7",
            "expected_improvement": "AbM7 between diatonic chords should favor C Harmonic Minor"
        }
    ]
    
    for case in test_cases:
        print(f"TEST CASE: {case['name']}")
        print(f"Progression: {case['progression']}")
        print(f"Key: {case['key']}")
        print(f"Focus: {case['focus_chord']}")
        print(f"Expected: {case['expected_improvement']}")
        print("-" * 40)
        
        chords = extract_chords(case['progression'])
        non_diatonic = detect_non_diatonic_notes(chords, case['key'])
        
        # Find the focus chord
        focus_chord_info = None
        for chord_info in non_diatonic:
            if chord_info['chord'] == case['focus_chord']:
                focus_chord_info = chord_info
                break
        
        if focus_chord_info:
            chord_notes = get_chord_components(case['focus_chord'])
            chord_index = chords.index(case['focus_chord'])
            
            # Get context notes
            context_notes = []
            if chord_index > 0:
                prev_notes = get_chord_components(chords[chord_index - 1])
                context_notes.extend(prev_notes)
            if chord_index < len(chords) - 1:
                next_notes = get_chord_components(chords[chord_index + 1])
                context_notes.extend(next_notes)
            
            context_notes = list(set(context_notes)) if context_notes else []
            
            print(f"Context notes: {context_notes}")
            
            # Get borrowed chord analysis with context
            borrowed_chords = find_borrowed_sources([focus_chord_info], case['key'], chords)
            borrowed = borrowed_chords[0]
            
            print(f"\nTOP 3 SOURCE CANDIDATES (with context enhancement):")
            for i, candidate in enumerate(borrowed.source_candidates[:3]):
                # Calculate confidence without context for comparison
                conf_without = calculate_key_confidence(chord_notes, candidate.key)
                conf_with = candidate.confidence
                boost = conf_with - conf_without
                
                print(f"  {i+1}. {candidate.key} ({candidate.relationship})")
                print(f"     Without context: {conf_without:.3f}")
                print(f"     With context: {conf_with:.3f}")
                print(f"     Context boost: {boost:+.3f}")
                
                # Show which notes contributed to the boost
                if context_notes:
                    key_notes = get_diatonic_notes(candidate.key)
                    matching_context = [note for note in context_notes if note in key_notes]
                    print(f"     Context notes in key: {matching_context}")
                print()
        
        print("=" * 60)
        print()

def show_implementation_summary():
    print("IMPLEMENTATION SUMMARY:")
    print("- Enhanced calculate_key_confidence() with context_notes parameter")
    print("- Added 7% weight for context chord notes (within 5-10% requested range)")
    print("- Modified find_borrowed_sources() to gather previous & next chord notes")
    print("- Context notes are deduplicated and passed to confidence calculation")
    print("- Harmonic context improves borrowed key candidate ranking accuracy")
    print()

if __name__ == "__main__":
    demonstrate_context_enhancement()
    show_implementation_summary()