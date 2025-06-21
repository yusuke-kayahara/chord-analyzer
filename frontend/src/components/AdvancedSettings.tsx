import React from 'react';
import { AdvancedSettings as AdvancedSettingsType } from '../types/chord';

interface AdvancedSettingsProps {
  settings: AdvancedSettingsType;
  onSettingsChange: (settings: AdvancedSettingsType) => void;
}

const AdvancedSettings: React.FC<AdvancedSettingsProps> = ({
  settings,
  onSettingsChange
}) => {
  const toggleAdvanced = () => {
    onSettingsChange({
      ...settings,
      showAdvanced: !settings.showAdvanced
    });
  };

  const handleAlgorithmChange = (algorithm: string) => {
    onSettingsChange({
      ...settings,
      algorithm
    });
  };

  const handleWeightChange = (type: 'traditional' | 'borrowed_chord' | 'triad_ratio', value: number) => {
    const newSettings = { ...settings };
    
    if (type === 'traditional') {
      newSettings.traditional_weight = value;
    } else if (type === 'borrowed_chord') {
      newSettings.borrowed_chord_weight = value;
    } else if (type === 'triad_ratio') {
      newSettings.triad_ratio_weight = value;
    }
    
    // 3つの重みの合計を1.0に正規化
    const total = newSettings.traditional_weight + newSettings.borrowed_chord_weight + newSettings.triad_ratio_weight;
    if (total > 0) {
      newSettings.traditional_weight /= total;
      newSettings.borrowed_chord_weight /= total;
      newSettings.triad_ratio_weight /= total;
    }
    
    onSettingsChange(newSettings);
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-6">
      <button
        type="button"
        onClick={toggleAdvanced}
        className="flex items-center justify-between w-full p-3 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors"
      >
        <span className="text-sm font-medium text-gray-700">
          詳細設定（アルゴリズム選択）
        </span>
        <svg 
          className={`w-4 h-4 text-gray-500 transition-transform ${settings.showAdvanced ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {settings.showAdvanced && (
        <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg space-y-4">
          {/* アルゴリズム選択 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              キー推定アルゴリズム
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="algorithm"
                  value="hybrid"
                  checked={settings.algorithm === 'hybrid'}
                  onChange={(e) => handleAlgorithmChange(e.target.value)}
                  className="mr-2"
                />
                <span className="text-sm">
                  <strong>ハイブリッド（推奨）</strong> - 借用和音最小化 + Krumhansl類似度
                </span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="algorithm"
                  value="borrowed_chord_minimal"
                  checked={settings.algorithm === 'borrowed_chord_minimal'}
                  onChange={(e) => handleAlgorithmChange(e.target.value)}
                  className="mr-2"
                />
                <span className="text-sm">
                  <strong>借用和音最小化</strong> - 借用和音が最も少ないキーを選択
                </span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="algorithm"
                  value="triad_ratio"
                  checked={settings.algorithm === 'triad_ratio'}
                  onChange={(e) => handleAlgorithmChange(e.target.value)}
                  className="mr-2"
                />
                <span className="text-sm">
                  <strong>トライアド比率分析</strong> - 1,3,5度の構成音比率が高いキーを選択
                </span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="algorithm"
                  value="traditional"
                  checked={settings.algorithm === 'traditional'}
                  onChange={(e) => handleAlgorithmChange(e.target.value)}
                  className="mr-2"
                />
                <span className="text-sm">
                  <strong>従来型</strong> - Krumhansl調性感プロファイル
                </span>
              </label>
            </div>
          </div>

          {/* 重み調整（ハイブリッドモード時のみ） */}
          {settings.algorithm === 'hybrid' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                アルゴリズム重み調整
              </label>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>トライアド比率分析</span>
                    <span>{(settings.triad_ratio_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.triad_ratio_weight}
                    onChange={(e) => handleWeightChange('triad_ratio', parseFloat(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>
                <div>
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>借用和音最小化</span>
                    <span>{(settings.borrowed_chord_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.borrowed_chord_weight}
                    onChange={(e) => handleWeightChange('borrowed_chord', parseFloat(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>
                <div>
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Krumhansl類似度</span>
                    <span>{(settings.traditional_weight * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.traditional_weight}
                    onChange={(e) => handleWeightChange('traditional', parseFloat(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>
              </div>
            </div>
          )}

          {/* 説明 */}
          <div className="p-3 bg-blue-50 rounded-md">
            <h4 className="text-sm font-medium text-blue-800 mb-1">アルゴリズムの特徴</h4>
            <ul className="text-xs text-blue-700 space-y-1">
              <li>• <strong>トライアド比率分析</strong>: キーの1,3,5度の構成音比率が高いキーを優先</li>
              <li>• <strong>借用和音最小化</strong>: より自然なキー（借用和音が少ない）を優先</li>
              <li>• <strong>従来型</strong>: 音楽理論に基づく統計的類似度を重視</li>
              <li>• <strong>ハイブリッド</strong>: 3つのアルゴリズムを組み合わせ、重み調整可能</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedSettings;