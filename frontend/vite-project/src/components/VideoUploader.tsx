import { useEffect, useState } from "react";
import { analyzeVideo } from "../services/api";

type AnalysisResult = {
  frames_processed: number;
  people_detected: number;
  hardhats_detected: number;
  no_hardhats_detected: number;
  safety_vests_detected: number;
  no_safety_vests_detected: number;
  no_masks_detected: number;
  ppe_compliance: number;
};

function VideoUploader() {
  const [video, setVideo] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);

  function handleVideoChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!file.type.startsWith("video/")) {
      setError("Please select a video file.");
      return;
    }

    setError("");
    setVideo(file);
    setResult(null);

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  }

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  async function handleAnalyze() {
    if (!video) {
      setError("Please select a video first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await analyzeVideo(video);

      setResult(data.results);
    } catch (error) {
      console.error(error);
      setError("Could not analyze the video.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="vision-container">
      <h1>NirmaanAI</h1>

      <h2>AI Safety Vision</h2>

      <p>
        Upload a construction-site video to analyze
        PPE compliance.
      </p>

      <input
        type="file"
        accept="video/*"
        onChange={handleVideoChange}
      />

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {previewUrl && (
        <div className="video-preview">
          <h3>Video Preview</h3>

          <video
            src={previewUrl}
            controls
            width="600"
          />
        </div>
      )}

      {video && (
        <button
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing video..."
            : "Analyze Video"}
        </button>
      )}

      {result && (
        <div className="results">

          <h2>Safety Analysis</h2>

          <div className="compliance">
            <h3>PPE Compliance</h3>

            <p>
              {result.ppe_compliance}%
            </p>
          </div>

          <div className="stats">

            <div>
              <strong>People Detected</strong>
              <p>{result.people_detected}</p>
            </div>

            <div>
              <strong>Hardhats Detected</strong>
              <p>{result.hardhats_detected}</p>
            </div>

            <div>
              <strong>Missing Hardhats</strong>
              <p>{result.no_hardhats_detected}</p>
            </div>

            <div>
              <strong>Safety Vests</strong>
              <p>{result.safety_vests_detected}</p>
            </div>

            <div>
              <strong>Missing Safety Vests</strong>
              <p>{result.no_safety_vests_detected}</p>
            </div>

            <div>
              <strong>Missing Masks</strong>
              <p>{result.no_masks_detected}</p>
            </div>

          </div>

          <p>
            Frames processed: {result.frames_processed}
          </p>

        </div>
      )}
    </div>
  );
}

export default VideoUploader;