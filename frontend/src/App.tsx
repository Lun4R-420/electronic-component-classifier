import { useState, type FormEvent, type ChangeEvent } from "react";
import "./App.css";
import Loading from "./Loading.tsx";

interface Detection {
  class_name: string;
  confidence: number;
  bounding_box: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [detectedObjects, setDetectedObjects] = useState<Detection[]>([]);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setDetectedObjects([]);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/detect", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setDetectedObjects(data.detections);
    setLoading(false);
    console.log("Detected Objects:", data.detections);
  }

  return (
    <div className="app-container">
      <div className="title">
        <h1>Electronic Component Detector</h1>
      </div>
      <div className="instructions">
        <h2>Add an image with electronic components and click "Detect" to identify them</h2>
      </div>
      <div>
        <form onSubmit={handleSubmit} className="upload-form">
          <input type="file" accept="image/*" onChange={handleFileChange} className="file-input" />
          <button type="submit" className="detect-button">
            Detect
          </button>
        </form>
      </div>
      {previewUrl && (
        <div className="preview-section">
          <h3>Preview</h3>
          <div className="image-container">
            <img src={previewUrl} alt="Preview" style={{ display: "block" }} />
            {detectedObjects.map((detection, index) => {
              const { x1, y1, x2, y2 } = detection.bounding_box;

              return (
                <div key={index}
                  style={{
                    position: "absolute",
                    left: `${x1 * 100}%`,
                    top: `${y1 * 100}%`,
                    width: `${(x2 - x1) * 100}%`,
                    height: `${(y2 - y1) * 100}%`,
                    border: "2px solid red",
                  }}>
                    <span className="label">
                      {detection.class_name}  ({detection.confidence})
                    </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {loading && <Loading/>}
    </div>
  );
}

export default App;