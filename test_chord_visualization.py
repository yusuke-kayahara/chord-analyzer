#!/usr/bin/env python3
"""
Test script for improved chord visualization with slash chord support
"""

def test_chord_visualization():
    print("=== Improved Chord Visualization Test ===\n")
    
    # Simulating the new logic
    def note_to_pc(note: str) -> int:
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        normalized = note.replace('Db', 'C#').replace('Eb', 'D#').replace('Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')
        return notes.index(normalized) if normalized in notes else -1
    
    def get_chord_root(chord: str) -> str:
        import re
        match = re.match(r'^([A-G][#b]?)', chord)
        return match.group(1) if match else ''
    
    def parse_slash_chord(chord: str):
        import re
        slash_match = re.match(r'^([^/]+)/([A-G][#b]?)$', chord)
        if slash_match:
            return {'main_chord': slash_match.group(1), 'bass_note': slash_match.group(2)}
        return {'main_chord': chord, 'bass_note': None}
    
    def get_chord_type(chord: str):
        root = get_chord_root(chord)
        remainder = chord[len(root):]
        
        import re
        if re.match(r'^m(?!aj)', remainder):
            extensions = remainder[1:]
            return {'quality': 'minor', 'extensions': extensions}
        elif re.match(r'^(dim|°)', remainder):
            extensions = re.sub(r'^(dim|°)', '', remainder)
            return {'quality': 'diminished', 'extensions': extensions}
        elif re.match(r'^(aug|\+)', remainder):
            extensions = re.sub(r'^(aug|\+)', '', remainder)
            return {'quality': 'augmented', 'extensions': extensions}
        else:
            return {'quality': 'major', 'extensions': remainder}
    
    def get_bass_note_degree(bass_note: str, key_root: str) -> str:
        key_pc = note_to_pc(key_root)
        bass_pc = note_to_pc(bass_note)
        
        if key_pc == -1 or bass_pc == -1:
            return '?'
        
        interval = (bass_pc - key_pc + 12) % 12
        degree_map = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII']
        return degree_map[interval]
    
    def analyze_chord_function(chord: str, main_key: str) -> str:
        key_parts = main_key.split(' ')
        if len(key_parts) < 2:
            return '?'
        
        key_root = key_parts[0]
        key_type = key_parts[1]
        
        # Parse slash chord
        slash_result = parse_slash_chord(chord)
        main_chord = slash_result['main_chord']
        bass_note = slash_result['bass_note']
        
        chord_root = get_chord_root(main_chord)
        if not chord_root:
            return '?'
        
        key_pc = note_to_pc(key_root)
        chord_pc = note_to_pc(chord_root)
        
        if key_pc == -1 or chord_pc == -1:
            return '?'
        
        interval = (chord_pc - key_pc + 12) % 12
        
        chord_type = get_chord_type(main_chord)
        quality = chord_type['quality']
        extensions = chord_type['extensions']
        
        major_degrees = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII']
        minor_degrees = ['i', 'bII', 'II', 'bIII', 'III', 'iv', '#iv', 'v', 'bVI', 'VI', 'bVII', 'vii']
        
        if key_type == 'Major':
            base_degree = major_degrees[interval]
            if quality == 'minor':
                base_degree = base_degree + 'm'  # 大文字のままで「m」を追加
            elif quality == 'diminished':
                base_degree = base_degree.lower() + '°'
            elif quality == 'augmented':
                base_degree = base_degree + '+'
        elif key_type == 'Minor':
            base_degree = minor_degrees[interval]
            if quality == 'major':
                base_degree = base_degree.upper()
            elif quality == 'diminished':
                base_degree = base_degree + '°'
            elif quality == 'augmented':
                base_degree = base_degree + '+'
        else:
            return '?'
        
        # Clean extensions
        clean_extensions = extensions
        if clean_extensions:
            import re
            clean_extensions = re.sub(r'[^0-9a-zA-Z+#bsumaj(),-]', '', clean_extensions)
        
        result = base_degree + clean_extensions
        
        # Add slash chord notation
        if bass_note:
            bass_degree = get_bass_note_degree(bass_note, key_root)
            result += '/' + bass_degree
        
        return result
    
    # Test cases
    test_cases = [
        # 修正対象のケース
        {'chord': 'FM7', 'key': 'C Major', 'expected': 'IVM7'},
        {'chord': 'FmM7', 'key': 'C Major', 'expected': 'IVmM7'},
        {'chord': 'Em7', 'key': 'C Major', 'expected': 'IIIm7'},
        {'chord': 'A7', 'key': 'C Major', 'expected': 'VI7'},
        
        # 基本的なマイナーコードテスト
        {'chord': 'Am7', 'key': 'C Major', 'expected': 'VIm7'},
        {'chord': 'Dm7', 'key': 'C Major', 'expected': 'IIm7'},
        {'chord': 'Bm7', 'key': 'C Major', 'expected': 'VIIm7'},
        
        # スラッシュコードテスト
        {'chord': 'C/E', 'key': 'C Major', 'expected': 'I/III'},
        {'chord': 'Am/C', 'key': 'C Major', 'expected': 'VIm/I'},
        
        # 複雑なコードテスト
        {'chord': 'Dm7b5', 'key': 'C Major', 'expected': 'IIm7b5'},
        {'chord': 'F#dim', 'key': 'C Major', 'expected': '#iv°'},
    ]
    
    for case in test_cases:
        result = analyze_chord_function(case['chord'], case['key'])
        status = "✓" if result == case['expected'] else "✗"
        print(f"{status} {case['chord']:>8} in {case['key']:>8} → {result:>10} (expected: {case['expected']})")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_chord_visualization()