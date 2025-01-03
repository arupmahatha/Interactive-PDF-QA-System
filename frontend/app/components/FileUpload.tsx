'use client';

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    try {
      const formData = new FormData();
      formData.append('file', acceptedFiles[0]);

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        onUploadSuccess();
      }
    } catch (error) {
      console.error('Upload failed:', error);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
  });

  return (
    <div
      {...getRootProps()}
      className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-gray-400"
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the PDF here...</p>
      ) : (
        <p>Drag and drop a PDF here, or click to select file</p>
      )}
    </div>
  );
} 