import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Shield, Box, Layout, Clock, TrendingUp, BadgeCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [detections, setDetections] = useState([]);
  const [stats, setStats] = useState({ count: 0, fps: 0 });
  const [lastUpdate, setLastUpdate] = useState(Date.now());
  const [isStreaming, setIsStreaming] = useState(true);
  const [streamSession, setStreamSession] = useState(Date.now());

  // Clear storage and handle stream session reset
  useEffect(() => {
    const clearCache = () => {
      localStorage.clear();
      sessionStorage.clear();
    };
    window.addEventListener('beforeunload', clearCache);
    
    if (isStreaming) {
      setStreamSession(Date.now());
    }

    return () => window.removeEventListener('beforeunload', clearCache);
  }, [isStreaming]);

  // Polling for detection metadata
  useEffect(() => {
    if (!isStreaming) return;

    const fetchDetections = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/detections`);
        setDetections(response.data.detections);
        setStats(prev => ({
          ...prev,
          count: response.data.count
        }));
        setLastUpdate(Date.now());
      } catch (error) {
        console.error("Error fetching detections:", error);
      }
    };

    const interval = setInterval(fetchDetections, 100); // 10Hz metadata polling
    return () => clearInterval(interval);
  }, [isStreaming]);

  return (
    <div className="app-container">
      <header className="glass">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <BadgeCheck  size={32} color="#ccccefff" />
          <h1 style={{color: "#ccccefff"}}>Object Detection System</h1>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button 
            onClick={() => setIsStreaming(!isStreaming)}
            className="glass"
            style={{
              padding: '0.5rem 1.5rem',
              color: isStreaming ? '#ef4444' : '#22c55e',
              border: `1px solid ${isStreaming ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.2)'}`,
              cursor: 'pointer',
              fontWeight: 600,
              borderRadius: '9999px',
              fontSize: '0.875rem',
              transition: 'all 0.2s ease'
            }}
          >
            {isStreaming ? 'Stop Stream' : 'Start Stream'}
          </button>
          <div className="status-badge" style={{ opacity: isStreaming ? 1 : 0.5 }}>
            <div className={isStreaming ? "status-dot" : ""} style={{ 
              width: 8, height: 8, borderRadius: '50%', 
              backgroundColor: isStreaming ? 'var(--status-live)' : '#64748b' 
            }} />
            {isStreaming ? 'SYSTEM LIVE' : 'STREAM PAUSED'}
          </div>
        </div>
      </header>

      <main className="dashboard-grid">
        {/* Left: Video Feed */}
        <section className="glass video-section">
          {isStreaming ? (
            <img 
              src={`${API_BASE_URL}/video_feed?t=${streamSession}`} 
              alt="Real-time object detection stream" 
              className="video-feed"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/1280x720?text=Waiting+for+Stream...';
              }}
            />
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
              <Layout size={64} style={{ opacity: 0.2, marginBottom: '1rem' }} />
              <p>Stream is currently inactive</p>
            </div>
          )}
          {isStreaming && (
            <div style={{
              position: 'absolute',
              bottom: '1rem',
              left: '1rem',
              padding: '0.5rem 1rem',
              background: 'rgba(0,0,0,0.6)',
              borderRadius: '0.5rem',
              fontSize: '0.75rem',
              color: '#fff',
              backdropFilter: 'blur(4px)'
            }}>
              1080p • 30 FPS • YOLO26 Nano
            </div>
          )}
        </section>

        {/* Right: Detections List */}
        <aside className="detection-sidebar">
          <div className="glass stat-card">
            <div className="card-title">
              <TrendingUp size={20} color="#6366f1" />
              Real-time Analytics
            </div>
            <div className="stat-value">{stats.count}</div>
            <div className="stat-label">Active Objects</div>
          </div>

          <div className="glass" style={{ padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
            <div className="card-title">
              <Activity size={20} color="#ec4899" />
              Detection Log
            </div>
            <div className="detection-list">
              <AnimatePresence mode="popLayout">
                {detections.length > 0 ? (
                  detections.map((det, index) => (
                    <motion.div
                      key={`${det.label}-${index}`}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      className="detection-item"
                    >
                      <div className="label-info">
                        <span className="label-name">{det.label.split(' ')[0]}</span>
                        <span className="label-meta">{det.label.split(' ')[1]} Confidence</span>
                      </div>
                      <div style={{
                        width: '12px',
                        height: '12px',
                        borderRadius: '3px',
                        backgroundColor: `rgb(${det.color[0]}, ${det.color[1]}, ${det.color[2]})`
                      }} />
                    </motion.div>
                  ))
                ) : (
                  <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                    Scanning environment...
                  </div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </aside>
      </main>

      <footer className="stats-grid">
        <div className="glass stat-card">
          <div className="stat-label">Latency</div>
          <div className="stat-value" style={{ fontSize: '1.25rem' }}>14ms</div>
        </div>
        <div className="glass stat-card">
          <div className="stat-label">Inference Engine</div>
          <div className="stat-value" style={{ fontSize: '1.25rem' }}>Ultralytics YOLO26</div>
        </div>
        <div className="glass stat-card">
          <div className="stat-label">Last Ping</div>
          <div className="stat-value" style={{ fontSize: '1.25rem' }}>
            {new Date(lastUpdate).toLocaleTimeString()}
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
