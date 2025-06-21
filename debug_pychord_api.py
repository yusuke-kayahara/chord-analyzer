#!/usr/bin/env python3
"""
pychordライブラリのAPI調査
"""
from pychord import Chord

def investigate_pychord():
    print("=== pychordライブラリ調査 ===")
    
    chord_symbol = "CM7"
    chord = Chord(chord_symbol)
    
    print(f"コード: {chord_symbol}")
    print(f"chord オブジェクト: {chord}")
    print(f"型: {type(chord)}")
    print(f"利用可能な属性・メソッド:")
    
    for attr in dir(chord):
        if not attr.startswith('_'):
            try:
                value = getattr(chord, attr)
                print(f"  {attr}: {value} (型: {type(value)})")
            except Exception as e:
                print(f"  {attr}: エラー - {e}")
    
    print(f"\n=== components()の詳細調査 ===")
    try:
        components = chord.components()
        print(f"components(): {components}")
        print(f"型: {type(components)}")
        
        if hasattr(components, '__iter__'):
            print("個別要素:")
            for i, comp in enumerate(components):
                print(f"  [{i}] {comp} (型: {type(comp)})")
                
                # 各要素の属性確認
                if hasattr(comp, '__dict__'):
                    print(f"    属性: {comp.__dict__}")
                    
                # name属性の確認
                if hasattr(comp, 'name'):
                    print(f"    name: {comp.name}")
                else:
                    print(f"    name属性なし - 直接文字列?: {str(comp)}")
    except Exception as e:
        print(f"components()エラー: {e}")

if __name__ == "__main__":
    investigate_pychord()