const API_URL = "http://127.0.0.1:8000";

export async function analyzeVideo(video: File) {
  const formData = new FormData();

  formData.append("video", video);

  const response = await fetch(
    `${API_URL}/api/vision/analyze-video`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error("Video analysis failed");
  }

  return response.json();
}