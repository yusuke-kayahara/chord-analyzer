import React, { useState, useEffect, useRef, useCallback } from 'react';
import * as Tone from 'tone';
import { ProgressionDetail } from '../types/chord';

interface PlaybackControlsProps {
  progression: ProgressionDetail[];
}

const PlaybackControls: React.FC<PlaybackControlsProps> = ({ progression }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentChordIndex, setCurrentChordIndex] = useState(-1);

  // useRef to hold Tone.js objects. This prevents them from being re-created on every render.
  const synthRef = useRef<Tone.PolySynth | null>(null);
  const sequenceRef = useRef<Tone.Sequence | null>(null);

  // Initialize synth only once when the component mounts
  useEffect(() => {
    console.log("Initializing synthesizer...");
    synthRef.current = new Tone.PolySynth(Tone.Synth, {
      oscillator: { type: 'fmsine', modulationType: 'sine', modulationIndex: 3, harmonicity: 3.4 },
      envelope: { attack: 0.01, decay: 0.1, sustain: 0.5, release: 1 }
    }).toDestination();

    // Cleanup on component unmount
    return () => {
      console.log("Disposing synthesizer on component unmount.");
      synthRef.current?.dispose();
      // Also ensure transport is stopped and cleaned up
      Tone.Transport.stop();
      Tone.Transport.cancel();
    };
  }, []);

  // This effect re-creates the sequence when the chord progression changes.
  useEffect(() => {
    // Clean up previous sequence if it exists
    if (sequenceRef.current) {
      console.log("Disposing old sequence.");
      sequenceRef.current.dispose();
    }
    // Stop transport and reset UI when progression changes
    Tone.Transport.stop();
    setIsPlaying(false);
    setCurrentChordIndex(-1);
    
    if (progression.length > 0 && synthRef.current) {
      console.log("Creating new sequence for progression:", progression);
      const newSequence = new Tone.Sequence(
        (time, chord) => {
          const notes = chord.components.map(n => `${n}4`);
          console.log(`[Tone.js] Playing ${chord.chord_symbol} at time ${time.toFixed(2)}`);
          synthRef.current?.triggerAttackRelease(notes, '1n', time);
          Tone.Draw.schedule(() => {
            setCurrentChordIndex(progression.indexOf(chord));
          }, time);
        },
        progression,
        '1n'
      );

      newSequence.loop = false; // Play only once
      sequenceRef.current = newSequence;
    }
  }, [progression]);

  const handlePlayPause = useCallback(async () => {
    if (!sequenceRef.current) {
      console.error("Playback attempted, but sequence is not ready.");
      return;
    }

    // IMPORTANT: Start AudioContext on user gesture
    if (Tone.context.state !== 'running') {
      try {
        await Tone.start();
        console.log("AudioContext started successfully!");
      } catch (e) {
        console.error("Failed to start AudioContext:", e);
        return; // Do not proceed if AudioContext fails to start
      }
    }

    if (isPlaying) {
      Tone.Transport.pause();
      setIsPlaying(false);
      console.log("Transport paused.");
    } else {
      // Start the transport and then start the sequence
      Tone.Transport.start();
      sequenceRef.current.start(0);
      setIsPlaying(true);
      console.log("Transport and sequence started.");
    }
  }, [isPlaying]);

  const handleStop = useCallback(() => {
    Tone.Transport.stop();
    // Reset UI state immediately on stop
    setIsPlaying(false);
    setCurrentChordIndex(-1);
    console.log("Transport stopped by user.");
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-gray-100 rounded-lg shadow-inner">
      <div className="flex items-center space-x-4">
        <button
          onClick={handlePlayPause}
          disabled={progression.length === 0}
          className="px-4 py-2 font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400"
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <button
          onClick={handleStop}
          disabled={progression.length === 0}
          className="px-4 py-2 font-semibold text-white bg-red-500 rounded-lg hover:bg-red-600 transition-colors disabled:bg-gray-400"
        >
          Stop
        </button>
        <div className="flex-grow flex items-center space-x-2 bg-gray-200 p-1 rounded-full">
          {progression.map((_, index) => (
            <div key={index} className="flex-1 h-3 rounded-full transition-colors"
                 style={{ backgroundColor: index === currentChordIndex ? '#3B82F6' : '#E5E7EB' }}>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlaybackControls;