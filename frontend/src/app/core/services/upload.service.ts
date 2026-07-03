import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

@Injectable({
  providedIn: 'root',
})
export class UploadService {

  private http = inject(HttpClient);

  uploadImage(
    claimId: number,
    file: File,
  ): Observable<any> {

    const formData = new FormData();

    formData.append(
      'file',
      file,
    );

    return this.http.post(
      `${API.BASE_URL}/upload/image/${claimId}`,
      formData,
    );

  }

  uploadDocument(
    claimId: number,
    file: File,
  ): Observable<any> {

    const formData = new FormData();

    formData.append(
      'document_type',
      'Insurance Policy',
    );

    formData.append(
      'file',
      file,
    );

    return this.http.post(
      `${API.BASE_URL}/upload/document/${claimId}`,
      formData,
    );

  }

  deleteDocument(documentId: number): Observable<void> {
    return this.http.delete<void>(`${API.BASE_URL}/claim-documents/${documentId}`);
  }

  deleteImage(imageId: number): Observable<void> {
    return this.http.delete<void>(`${API.BASE_URL}/claim-images/${imageId}`);
  }
}