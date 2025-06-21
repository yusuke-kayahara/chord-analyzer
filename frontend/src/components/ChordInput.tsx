import React, { useState, useEffect } from 'react';

interface ChordInputProps {
  onAnalyze: (chordInput: string) => void;
  isAnalyzing: boolean;
  initialInput?: string; // 外部から初期値を設定可能
}

const ChordInput: React.FC<ChordInputProps> = ({ onAnalyze, isAnalyzing, initialInput = '' }) => {
  const [input, setInput] = useState(initialInput);
  const [examples] = useState([
    '[CM7][Am7][FM7][G7]',
    '[C][Am][Fm][G]', 
    '[FM7][FmM7][Em7][A7]',
    '[C][Ab][F][G]',
    '[Am][F][C][G]'
  ]);

  // 外部から初期値が変更された時に入力フィールドを更新
  useEffect(() => {
    setInput(initialInput);
  }, [initialInput]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isAnalyzing) {
      onAnalyze(input.trim());
    }
  };

  const handleExampleClick = (example: string) => {
    setInput(example);
  };

  const isValidInput = input.trim().length > 0;

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <p className="text-gray-600">
          []で囲まれたコードネームを入力してください。借用和音を自動検出します。
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="chord-input" className="block text-sm font-medium text-gray-700 mb-2">
            コード進行
          </label>
          <textarea
            id="chord-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="例: [CM7][Am7][FM7][G7]"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
            rows={3}
            disabled={isAnalyzing}
          />
        </div>

        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-gray-600 self-center">例:</span>
          {examples.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              disabled={isAnalyzing}
              className="chord-button text-sm"
            >
              {example}
            </button>
          ))}
        </div>

        <button
          type="submit"
          disabled={!isValidInput || isAnalyzing}
          className="w-full py-3 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isAnalyzing ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              分析中...
            </div>
          ) : (
            '分析開始'
          )}
        </button>
      </form>
    </div>
  );
};

export default ChordInput;