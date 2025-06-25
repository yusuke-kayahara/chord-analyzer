#!/usr/bin/env python3
"""
テンションコード対応のテストケース
"""

def test_tension_chord_parsing():
    print("=== テンションコード解析テスト ===\n")
    
    # テンション解析ロジックをシミュレート
    import re
    
    def parse_tension_chord(chord: str):
        # テンション部分を抽出
        tension_match = re.match(r'^([A-G][#b]?[^(]*)\(([^)]+)\)$', chord)
        
        if tension_match:
            main_chord = tension_match.group(1)
            tension_part = tension_match.group(2)
            
            # カンマで分割してテンション要素を取得
            tension_elements = re.split(r'[,、\s]+', tension_part)
            tension_elements = [t.strip() for t in tension_elements if t.strip()]
            
            # 各テンション要素をクリーンアップ
            tensions = []
            for element in tension_elements:
                tension_match = re.match(r'([#b+-]?\d+)', element)
                if tension_match:
                    tensions.append(tension_match.group(1))
                else:
                    tensions.append(element)
            
            return {'main_chord': main_chord, 'tensions': tensions}
        
        return {'main_chord': chord, 'tensions': []}
    
    def parse_slash_chord(chord: str):
        slash_match = re.match(r'^([^/]+)/([A-G][#b]?)$', chord)
        if slash_match:
            return {'main_chord': slash_match.group(1), 'bass_note': slash_match.group(2)}
        return {'main_chord': chord, 'bass_note': None}
    
    def get_chord_root(chord: str) -> str:
        match = re.match(r'^([A-G][#b]?)', chord)
        return match.group(1) if match else ''
    
    def get_chord_type(chord: str):
        root = get_chord_root(chord)
        remainder = chord[len(root):]
        
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
    
    def analyze_tension_chord(chord: str, main_key: str = 'C Major') -> str:
        print(f"解析: {chord}")
        
        # オンコード分析
        slash_result = parse_slash_chord(chord)
        main_chord = slash_result['main_chord']
        bass_note = slash_result['bass_note']
        print(f"  オンコード分析: main={main_chord}, bass={bass_note}")
        
        # テンション分析
        tension_result = parse_tension_chord(main_chord)
        core_chord = tension_result['main_chord']
        tensions = tension_result['tensions']
        print(f"  テンション分析: core={core_chord}, tensions={tensions}")
        
        # コードタイプ分析
        chord_type = get_chord_type(core_chord)
        print(f"  コードタイプ: {chord_type}")
        
        # 度数計算（簡易版）
        root = get_chord_root(core_chord)
        key_root = main_key.split()[0]
        
        # 度数マッピング（Cメジャーキー固定）
        root_to_degree = {
            'C': 'I', 'D': 'II', 'E': 'III', 'F': 'IV', 
            'G': 'V', 'A': 'VI', 'B': 'VII'
        }
        
        base_degree = root_to_degree.get(root, '?')
        
        # コード性質を反映
        if chord_type['quality'] == 'minor':
            result = base_degree + 'm'
        elif chord_type['quality'] == 'diminished':
            result = base_degree.lower() + '°'
        elif chord_type['quality'] == 'augmented':
            result = base_degree + '+'
        else:
            result = base_degree
        
        # エクステンションを追加
        if chord_type['extensions']:
            clean_ext = re.sub(r'[^0-9a-zA-Z+#bsumaj(),-]', '', chord_type['extensions'])
            result += clean_ext
        
        # テンション追加
        if tensions:
            result += '(' + ','.join(tensions) + ')'
        
        # オンコード追加
        if bass_note:
            bass_degree = root_to_degree.get(bass_note, '?')
            result += '/' + bass_degree
        
        print(f"  最終結果: {result}")
        print()
        return result
    
    # テストケース
    test_cases = [
        # 基本的なテンションコード
        'C7(9)',
        'Dm7(11)',
        'FM7(#11)',
        'G7(b9)',
        
        # 複数テンション
        'C7(9,11)',
        'Dm7(b9,#11)',
        'Am7(9、13)',  # 日本語カンマ
        
        # 複雑なテンション
        'G7(b9,#9,#11,b13)',
        'FM7(9,#11,13)',
        
        # オンコード + テンション
        'C7(9)/E',
        'Dm7(11)/F',
        
        # マイナーコード + テンション
        'Am7(b9)',
        'Fm7(11)',
        'Em7(b5)',
    ]
    
    print("テストケース実行:")
    for chord in test_cases:
        result = analyze_tension_chord(chord)
    
    print("=== 期待される結果例 ===")
    expected_results = {
        'C7(9)': 'I7(9)',
        'Dm7(11)': 'IIm7(11)', 
        'FM7(#11)': 'IVM7(#11)',
        'G7(b9)': 'V7(b9)',
        'C7(9,11)': 'I7(9,11)',
        'Am7(9、13)': 'VIm7(9,13)',
        'C7(9)/E': 'I7(9)/III',
        'Am7(b9)': 'VIm7(b9)',
    }
    
    for chord, expected in expected_results.items():
        print(f"  {chord:>12} → {expected}")

if __name__ == "__main__":
    test_tension_chord_parsing()