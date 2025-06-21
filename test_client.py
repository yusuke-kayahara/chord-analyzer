#!/usr/bin/env python3
"""
APIクライアントテスト
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # ① ルートエンドポイントのテスト
    try:
        response = requests.get(f"{base_url}/")
        print("=== ルートエンドポイント ===")
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        print()
    except Exception as e:
        print(f"ルートエンドポイントエラー: {e}")
        return False
    
    # ② /analyzeエンドポイントのテスト
    test_cases = [
        {
            "name": "基本的なコード進行",
            "input": "[CM7][Am7][FM7][G7]"
        },
        {
            "name": "借用和音を含む進行",
            "input": "[FM7][FmM7][Em7][A7]"
        },
        {
            "name": "シンプルなトライアド",
            "input": "[C][F][G][C]"
        },
        {
            "name": "マイナーキー進行",
            "input": "[Am][F][C][G]"
        }
    ]
    
    print("=== /analyze エンドポイントテスト ===")
    for test_case in test_cases:
        try:
            payload = {"chord_input": test_case["input"]}
            response = requests.post(f"{base_url}/analyze", json=payload)
            
            print(f"\n【{test_case['name']}】")
            print(f"入力: {test_case['input']}")
            print(f"ステータス: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"推定キー: {result['main_key']}")
                print(f"信頼度: {result['confidence']:.3f}")
                print(f"借用和音数: {len(result['borrowed_chords'])}")
                
                # ピッチクラスベクトルの表示（簡略化）
                vector = result['pitch_class_vector']
                non_zero = [(i, v) for i, v in enumerate(vector) if v > 0]
                print(f"主要構成音: {[(i, f'{v:.3f}') for i, v in non_zero[:5]]}")
            else:
                print(f"エラー: {response.text}")
                
        except Exception as e:
            print(f"テストエラー [{test_case['name']}]: {e}")
    
    print("\n✓ APIテスト完了")
    return True

if __name__ == "__main__":
    print("Chord Analyzer API - クライアントテスト")
    print("=" * 50)
    
    # requests ライブラリの確認
    try:
        import requests
    except ImportError:
        print("requestsライブラリが必要です: pip install requests")
        exit(1)
    
    test_api()