import React, { useState, useEffect } from 'react';

const ImageComponent = () => {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    // Replace 'YOUR_BACKEND_ENDPOINT' with the actual endpoint to fetch the image
    const backendEndpoint = 'YOUR_BACKEND_ENDPOINT';

    // Fetch the image from the backend
    fetch(backendEndpoint)
      .then((response) => response.blob())
      .then((blob) => {
        const objectURL = URL.createObjectURL(blob);
        setImageData(objectURL);
      })
      .catch((error) => {
        console.error('Error fetching image:', error);
      });
  }, []);

  return (
    <div>
      {imageData && <img src={imageData} alt="Backend Image" style={{ maxWidth: '100%' }} />}
      {!imageData && <p>Loading image...</p>}
    </div>
  );
};

export default ImageComponent;
