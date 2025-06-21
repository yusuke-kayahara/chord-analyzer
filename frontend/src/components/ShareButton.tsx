import React, { useState } from 'react';
import { AdvancedSettings } from '../types/chord';
import { URLSharing } from '../utils/urlSharing';

interface ShareButtonProps {
  chordInput: string;
  settings: AdvancedSettings;
}

const ShareButton: React.FC<ShareButtonProps> = ({ chordInput, settings }) => {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const shareURL = URLSharing.encodeAnalysisToURL(chordInput, settings);
    const success = await URLSharing.copyToClipboard(shareURL);
    
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // 2秒後にリセット
    }
  };

  return (
    <button
      onClick={handleShare}
      className="flex items-center space-x-2 px-4 py-2 bg-green-100 hover:bg-green-200 text-green-800 rounded-lg transition-colors duration-200"
      title="分析結果のURLをコピーして共有"
    >
      <svg 
        className="w-4 h-4" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" 
        />
      </svg>
      <span className="text-sm font-medium">
        {copied ? 'URLをコピーしました！' : '結果を共有'}
      </span>
    </button>
  );
};

export default ShareButton;