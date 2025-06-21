import React, { useState, useEffect } from 'react';
import ChordInput from './components/ChordInput';
import AnalysisResult from './components/AnalysisResult';
import ChordVisualization from './components/ChordVisualization';
import { analyzeChordProgression, testApiConnection } from './services/api';
import { UIState } from './types/chord';

function App() {
  const [state, setState] = useState<UIState>({
    isAnalyzing: false,
    error: null,
    result: null,
  });
  const [lastInput, setLastInput] = useState<string>('');
  const [apiConnected, setApiConnected] = useState<boolean>(false);

  // API接続テスト
  useEffect(() => {
    const checkConnection = async () => {
      const connected = await testApiConnection();
      setApiConnected(connected);
    };
    checkConnection();
  }, []);

  const handleAnalyze = async (chordInput: string) => {
    setState(prev => ({ ...prev, isAnalyzing: true, error: null }));
    setLastInput(chordInput);

    try {
      const result = await analyzeChordProgression(chordInput);
      setState(prev => ({
        ...prev,
        isAnalyzing: false,
        result,
        error: null,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isAnalyzing: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      }));
    }
  };

  const clearResults = () => {
    setState({
      isAnalyzing: false,
      error: null,
      result: null,
    });
    setLastInput('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                コード進行分析ツール
              </h1>
              <p className="mt-1 text-gray-600">
                借用和音を自動検出・分析する音楽理論アプリケーション
              </p>
            </div>
            <div className="flex items-center space-x-4">
              {/* API接続状態 */}
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  apiConnected ? 'bg-green-500' : 'bg-red-500'
                }`}></div>
                <span className="text-sm text-gray-600">
                  API {apiConnected ? '接続中' : '未接続'}
                </span>
              </div>
              
              {/* クリアボタン */}
              {state.result && (
                <button
                  onClick={clearResults}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                >
                  新規分析
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        {/* API未接続エラー */}
        {!apiConnected && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-medium text-red-800">API接続エラー</h3>
                <p className="text-sm text-red-700">
                  バックエンドAPIに接続できません。http://localhost:8000 でサーバーが起動していることを確認してください。
                </p>
              </div>
            </div>
          </div>
        )}

        {/* エラー表示 */}
        {state.error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-medium text-red-800">分析エラー</h3>
                <p className="text-sm text-red-700">{state.error}</p>
              </div>
            </div>
          </div>
        )}

        {/* コード入力 */}
        <ChordInput
          onAnalyze={handleAnalyze}
          isAnalyzing={state.isAnalyzing}
        />

        {/* 分析結果 */}
        {state.result && (
          <>
            <AnalysisResult result={state.result} />
            <ChordVisualization
              chordInput={lastInput}
              mainKey={state.result.main_key}
              borrowedChords={state.result.borrowed_chords}
            />
          </>
        )}

        {/* 機能紹介（結果がない場合） */}
        {!state.result && !state.isAnalyzing && (
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">キー推定</h3>
              <p className="text-gray-600 text-sm">
                Krumhanslの調性感プロファイルを使用して、コード進行から高精度でキーを推定します。
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">借用和音検出</h3>
              <p className="text-gray-600 text-sm">
                非ダイアトニック音を分析し、借用元のキーと音楽理論的関係を特定します。
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">視覚化</h3>
              <p className="text-gray-600 text-sm">
                コード進行と借用和音を直感的に理解できるビジュアル表示を提供します。
              </p>
            </div>
          </div>
        )}
      </main>

      {/* フッター */}
      <footer className="bg-gray-50 border-t mt-16">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="text-center">
            <p className="text-gray-600 text-sm">
              Powered by FastAPI + React | 音楽理論に基づく高精度分析
            </p>
            <p className="text-gray-500 text-xs mt-1">
              Phase 1: キー推定 ✓ | Phase 2: 借用和音検出 ✓ | Phase 3: フロントエンド ✓
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
