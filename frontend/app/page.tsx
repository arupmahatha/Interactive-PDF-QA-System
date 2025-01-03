'use client';

import { useState } from 'react';
import FileUpload from './components/FileUpload';
import Chat from './components/Chat';

export default function Home() {
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-8">PDF Question Answering System</h1>
      
      <div className="space-y-8">
        <FileUpload onUploadSuccess={() => setIsFileUploaded(true)} />
        
        {isFileUploaded && <Chat />}
      </div>
    </main>
  );
} 