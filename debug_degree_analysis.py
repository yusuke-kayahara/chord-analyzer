#!/usr/bin/env python3
"""
Debug script for chord degree analysis
"""

import sys
import os
sys.path.append('/home/kyhrysk/chord-analyzer/frontend/src')

def debug_chord_degrees():
    # Simulate the ChordVisualization logic
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def note_to_pc(note: str) -> int:
        normalized = note.replace('Db', 'C#').replace('Eb', 'D#').replace('Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')
        return NOTES.index(normalized) if normalized in NOTES else -1
    
    def get_chord_root(chord: str) -> str:
        import re
        match = re.match(r'^([A-G][#b]?)', chord)
        return match.group(1) if match else ''
    
    def analyze_chord_function(chord: str, main_key: str) -> str:
        key_parts = main_key.split(' ')
        if len(key_parts) < 2:
            return '?'
        
        key_root = key_parts[0]
        key_type = key_parts[1]
        
        chord_root = get_chord_root(chord)
        if not chord_root:
            return '?'
        
        key_pc = note_to_pc(key_root)
        chord_pc = note_to_pc(chord_root)
        
        if key_pc == -1 or chord_pc == -1:
            return '?'
        
        # キーからの度数を計算
        interval = (chord_pc - key_pc + 12) % 12
        
        print(f"Chord: {chord}")
        print(f"  Root: {chord_root} (PC: {chord_pc})")
        print(f"  Key: {main_key} - Root: {key_root} (PC: {key_pc})")
        print(f"  Interval: {interval}")
        
        # メジャーキーでの度数マッピング
        major_degrees = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII']
        
        if key_type == 'Major':
            degree = major_degrees[interval]
            print(f"  Degree: {degree}")
            return degree
        
        return '?'
    
    # Test the problematic progression
    print("=== Testing [FM7][E7][Am7][C7] ===")
    chords = ['FM7', 'E7', 'Am7', 'C7']
    main_key = 'C Major'
    
    for chord in chords:
        result = analyze_chord_function(chord, main_key)
        print(f"Result: {result}")
        print("-" * 30)

if __name__ == "__main__":
    debug_chord_degrees()