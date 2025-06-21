import React, { useState, useEffect, useCallback } from 'react';
import ChordInput from './components/ChordInput';
import AnalysisResult from './components/AnalysisResult';
import ChordVisualization from './components/ChordVisualization';
import AdvancedSettings from './components/AdvancedSettings';
import AnalysisHistory from './components/AnalysisHistory';
import ShareButton from './components/ShareButton';
import { analyzeChordProgression, testApiConnection } from './services/api';
import { UIState, AdvancedSettings as AdvancedSettingsType } from './types/chord';
import { HistoryStorage } from './utils/historyStorage';
import { URLSharing } from './utils/urlSharing';

function App() {
  const [state, setState] = useState<UIState>({
    isAnalyzing: false,
    error: null,
    result: null,
  });
  const [lastInput, setLastInput] = useState<string>('');
  const [apiConnected, setApiConnected] = useState<boolean | null>(null); // null: 未テスト, true: 接続, false: 未接続
  const [advancedSettings, setAdvancedSettings] = useState<AdvancedSettingsType>({
    algorithm: 'hybrid',
    traditional_weight: 0.2,
    borrowed_chord_weight: 0.3,
    triad_ratio_weight: 0.5,
    manual_key: '',
    showAdvanced: false
  });

  const handleAnalyze = useCallback(async (chordInput: string, saveToHistory: boolean = true) => {
    setState(prev => ({ ...prev, isAnalyzing: true, error: null }));
    setLastInput(chordInput);

    try {
      const result = await analyzeChordProgression(
        chordInput,
        advancedSettings.algorithm,
        advancedSettings.traditional_weight,
        advancedSettings.borrowed_chord_weight,
        advancedSettings.triad_ratio_weight,
        advancedSettings.manual_key
      );
      setState(prev => ({
        ...prev,
        isAnalyzing: false,
        result,
        error: null,
      }));
      
      // 新規分析の場合のみ履歴に保存
      if (saveToHistory) {
        HistoryStorage.saveAnalysis(chordInput, advancedSettings, result);
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isAnalyzing: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      }));
    }
  }, [advancedSettings]);

  const clearResults = () => {
    setState({
      isAnalyzing: false,
      error: null,
      result: null,
    });
    setLastInput('');
  };

  const handleReplayAnalysis = (chordInput: string, settings: AdvancedSettingsType) => {
    // 設定を復元
    setAdvancedSettings(settings);
    // 分析を再実行（履歴には保存しない）
    handleAnalyze(chordInput, false);
  };

  // API接続テスト
  useEffect(() => {
    const checkConnection = async () => {
      const connected = await testApiConnection();
      setApiConnected(connected);
    };
    checkConnection();
  }, []);

  // URL共有からの復元機能
  useEffect(() => {
    const urlData = URLSharing.decodeAnalysisFromURL();
    if (urlData) {
      const { chordInput, settings } = urlData;
      
      // 設定を復元
      setAdvancedSettings(settings);
      
      // 分析を自動実行（履歴には保存しない）
      setTimeout(() => {
        handleAnalyze(chordInput, false);
      }, 500); // API接続確認後に実行
      
      // URLパラメータをクリア（任意）
      // URLSharing.clearURLParams();
    }
  }, [handleAnalyze]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900 text-center">
            コード進行分析ツール
          </h1>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        {/* API未接続エラー（接続テスト完了後のみ表示） */}
        {apiConnected === false && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-medium text-red-800">API接続エラー</h3>
                <p className="text-sm text-red-700">
                  バックエンドAPIに接続できません。しばらく時間をおいて再度お試しください。
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

        {/* 詳細設定 */}
        <AdvancedSettings
          settings={advancedSettings}
          onSettingsChange={setAdvancedSettings}
        />

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
            
            {/* 共有ボタン */}
            <div className="w-full max-w-4xl mx-auto flex justify-center mb-4">
              <ShareButton 
                chordInput={lastInput}
                settings={advancedSettings}
              />
            </div>
            
            {/* 使い方のヒント */}
            <div className="w-full max-w-4xl mx-auto p-4 bg-blue-50 rounded-md">
              <h3 className="text-sm font-medium text-blue-800 mb-2">使い方のヒント</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• コードは []で囲んで入力してください</li>
                <li>• 例: [CM7][Am7][Fm][G7] → FmがC Minorからの借用和音として検出されます</li>
                <li>• 複雑なコード（テンション含む）も対応: [FM7(13)][FmM7]</li>
                <li>• セカンダリドミナント（V/ii等）も自動検出されます</li>
              </ul>
            </div>
          </>
        )}

        {/* 分析履歴 */}
        <AnalysisHistory onReplayAnalysis={handleReplayAnalysis} />

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
