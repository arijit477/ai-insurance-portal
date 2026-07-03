import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API } from '../constants/api';

import { LoginRequest } from '../models/auth/login-request';
import { RegisterRequest } from '../models/auth/register-request';
import { AuthResponse } from '../models/auth/auth-response';
import { User } from '../models/auth/user';

import { TokenService } from './token.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private http = inject(HttpClient);

  private tokenService = inject(TokenService);

  private readonly baseUrl = API.BASE_URL;

  register(
    request: RegisterRequest,
  ): Observable<User> {

    return this.http.post<User>(
      `${this.baseUrl}${API.AUTH.REGISTER}`,
      request,
    );

  }

  login(
    request: LoginRequest,
  ): Observable<AuthResponse> {

    return this.http.post<AuthResponse>(
      `${this.baseUrl}${API.AUTH.LOGIN}`,
      request,
    );

  }

  getProfile(): Observable<User> {

    return this.http.get<User>(
      `${this.baseUrl}${API.AUTH.PROFILE}`,
    );

  }

  saveToken(
    token: string,
  ): void {

    this.tokenService.setToken(token);

  }

  getToken(): string | null {

    return this.tokenService.getToken();

  }

  logout(): void {

    this.tokenService.removeToken();

  }

  isLoggedIn(): boolean {

    return this.tokenService.isLoggedIn();

  }

}