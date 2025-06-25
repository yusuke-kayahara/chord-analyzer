#!/usr/bin/env python3
"""
テンションコード記法の調査・分析
"""

def analyze_tension_notation():
    print("=== テンションコード記法の調査 ===\n")
    
    # 一般的なテンションコード記法パターン
    tension_examples = [
        # 基本的なテンション
        "C(9)", "C(11)", "C(13)",
        "Cm(9)", "Cm(11)", "Cm(13)",
        
        # 複数テンション
        "C(9,11)", "C(9,13)", "C(11,13)",
        "C(9、11)", "C(9、13)",  # 日本語カンマ
        
        # 変化テンション
        "C(b9)", "C(#9)", "C(+9)", "C(-9)",
        "C(#11)", "C(b13)",
        
        # 複雑なテンション
        "C(b9,#11)", "C(#9,b13)", "C(9,#11,13)",
        "C(b9、#11、13)",
        
        # 7thコード + テンション
        "C7(9)", "CM7(9)", "Cm7(9)", "CmM7(9)",
        "C7(b9)", "C7(#9)", "C7(#11)", "C7(b13)",
        "CM7(#11)", "Cm7(11)",
        
        # sus + テンション
        "Csus4(9)", "Csus2(11)",
        
        # 特殊記法
        "C9", "C11", "C13",  # ()なしの記法
        "C7add9", "Cadd9",   # add記法
        "C7(9,11,13)",       # 全テンション
    ]
    
    print("テンションコード記法パターン:")
    for i, example in enumerate(tension_examples, 1):
        print(f"{i:2d}. {example}")
    
    print("\n=== テンション記法の分析 ===")
    
    print("\n1. 基本構造:")
    print("   コードルート + 品質 + (テンション)")
    print("   例: C7(b9,#11) = C + 7 + (b9,#11)")
    
    print("\n2. テンション記号:")
    print("   - 9, 11, 13: ナチュラルテンション")
    print("   - b9, #9, +9, -9: 変化9th")
    print("   - #11: 変化11th")  
    print("   - b13: 変化13th")
    
    print("\n3. 区切り文字:")
    print("   - , (カンマ): C(9,11)")
    print("   - 、(日本語カンマ): C(9、11)")
    print("   - スペース: C(9 11) [稀]")
    
    print("\n4. 省略記法:")
    print("   - C9 = C7(9)")
    print("   - C11 = C7(9,11)")
    print("   - C13 = C7(9,11,13)")
    
    print("\n5. 特殊ケース:")
    print("   - add9: メジャー7thなしの9th")
    print("   - omit: 特定音の省略")
    print("   - alt: オルタードテンション")

def design_tension_parser():
    print("\n=== テンション解析ロジックの設計 ===\n")
    
    print("1. 解析ステップ:")
    print("   a) メインコード部分とテンション部分を分離")
    print("   b) テンション部分から()内を抽出")
    print("   c) カンマで分割してテンション要素を取得")
    print("   d) 各テンション要素を解析")
    
    print("\n2. 正規表現パターン:")
    print("   メインコード: ^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7)?)")
    print("   テンション: \\(([^)]+)\\)")
    print("   テンション要素: ([#b+-]?\\d+)")
    
    print("\n3. テンション要素の処理:")
    print("   - 数字部分: 9, 11, 13")
    print("   - 変化記号: #, b, +, -")
    print("   - 組み合わせ: #9, b13, +11")
    
    print("\n4. 度数表示への統合:")
    print("   - ベースコード度数 + テンション情報")
    print("   - 例: IVM7(9,#11) = IV + M7 + (9,#11)")

def test_tension_parsing():
    print("\n=== テンション解析テスト ===\n")
    
    import re
    
    def parse_tension_chord(chord: str):
        print(f"解析対象: {chord}")
        
        # メインコード部分とテンション部分を分離
        main_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7)?)', chord)
        tension_match = re.search(r'\(([^)]+)\)', chord)
        
        if main_match:
            main_chord = main_match.group(1)
            print(f"  メインコード: {main_chord}")
        else:
            print(f"  メインコード: 解析失敗")
            return
        
        if tension_match:
            tension_part = tension_match.group(1)
            print(f"  テンション部分: {tension_part}")
            
            # テンション要素を分割
            tension_elements = re.split(r'[,、\s]+', tension_part)
            tension_elements = [t.strip() for t in tension_elements if t.strip()]
            
            print(f"  テンション要素: {tension_elements}")
            
            # 各テンション要素を解析
            parsed_tensions = []
            for element in tension_elements:
                tension_match = re.match(r'([#b+-]?)(\d+)', element)
                if tension_match:
                    modifier = tension_match.group(1) if tension_match.group(1) else ''
                    number = tension_match.group(2)
                    parsed_tensions.append(f"{modifier}{number}")
            
            print(f"  解析済みテンション: {parsed_tensions}")
        else:
            print(f"  テンション: なし")
        
        print()
    
    # テストケース
    test_chords = [
        "C7(9)",
        "Dm7(b9,#11)",
        "FM7(9、13)",
        "Am7(11)",
        "G7(b9,#9,#11,b13)",
        "Csus4(9)",
        "BbM7(#11)"
    ]
    
    for chord in test_chords:
        parse_tension_chord(chord)

if __name__ == "__main__":
    analyze_tension_notation()
    design_tension_parser()
    test_tension_parsing()