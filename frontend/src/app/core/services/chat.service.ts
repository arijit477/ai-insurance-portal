import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

import {
  ChatRequest,
  ChatResponse,
} from '../models/chat';

@Injectable({
  providedIn: 'root',
})
export class ChatService {

  private http = inject(HttpClient);

  ask(
    request: ChatRequest,
  ): Observable<ChatResponse> {

    return this.http.post<ChatResponse>(
      `${API.BASE_URL}/api/v1/chat`,
      request,
    );

  }
}