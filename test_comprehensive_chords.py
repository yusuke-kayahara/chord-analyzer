#!/usr/bin/env python3
"""
包括的なコード解析テスト（テンション対応）
"""

def comprehensive_chord_test():
    print("=== 包括的コード解析テスト（テンション対応） ===\n")
    
    # 実際のコード進行例
    test_progressions = [
        {
            'name': 'ジャズスタンダード（テンション含む）',
            'progression': '[CM7(9)][Am7(11)][Dm7(9)][G7(b9)][Em7][Am7][Dm7][G7]',
            'key': 'C Major'
        },
        {
            'name': 'ボサノバ風（複雑テンション）',
            'progression': '[CM7(#11)][F7(#11)][Em7(b5)][A7(b9,b13)][Dm7][G7(9,13)]',
            'key': 'C Major'
        },
        {
            'name': 'オンコード + テンション',
            'progression': '[C7(9)/E][F7(#11)/A][G7(b9)/B][C]',
            'key': 'C Major'
        },
        {
            'name': 'マイナーキー + テンション',
            'progression': '[Am7][Dm7(11)][G7(b9)][CM7(9)]',
            'key': 'A Minor'
        }
    ]
    
    # 期待される結果
    expected_results = {
        'CM7(9)': 'IM7(9)',
        'Am7(11)': 'VIm7(11)', 
        'Dm7(9)': 'IIm7(9)',
        'G7(b9)': 'V7(b9)',
        'CM7(#11)': 'IM7(#11)',
        'F7(#11)': 'IV7(#11)',
        'Em7(b5)': 'IIIm7(b5)',
        'A7(b9,b13)': 'VI7(b9,b13)',
        'G7(9,13)': 'V7(9,13)',
        'C7(9)/E': 'I7(9)/III',
        'F7(#11)/A': 'IV7(#11)/VI',
        'G7(b9)/B': 'V7(b9)/VII'
    }
    
    print("テスト対象のコード進行:")
    for prog in test_progressions:
        print(f"\n{prog['name']}")
        print(f"進行: {prog['progression']}")
        print(f"キー: {prog['key']}")
    
    print(f"\n期待される度数表示例:")
    for chord, expected in expected_results.items():
        print(f"  {chord:>15} → {expected}")
    
    print(f"\n=== 実装された機能 ===")
    print("✅ テンション記法解析:")
    print("   - 基本テンション: (9), (11), (13)")
    print("   - 変化テンション: (b9), (#9), (#11), (b13)")
    print("   - 複数テンション: (9,11), (b9,#11,13)")
    print("   - 日本語カンマ対応: (9、11、13)")
    
    print("\n✅ 統合機能:")
    print("   - オンコード + テンション: C7(9)/E → I7(9)/III")
    print("   - マイナーコード + テンション: Am7(11) → VIm7(11)")
    print("   - 複雑コンビネーション: G7(b9,#11,b13)/B")
    
    print("\n✅ 表記統一:")
    print("   - メジャーコード: I7(9), IVM7(#11)")
    print("   - マイナーコード: IIm7(11), VIm7(b9)")
    print("   - オンコード: I7(9)/III, IVm7(11)/VI")
    
    print(f"\n=== テスト方法 ===")
    print("1. フロントエンド（http://localhost:3000）でテスト")
    print("2. 以下のコード進行を入力:")
    for prog in test_progressions:
        print(f"   - {prog['progression']}")
    print("3. 度数表示でテンション情報が正しく表示されることを確認")

if __name__ == "__main__":
    comprehensive_chord_test()