export interface ChatRequest {

  claim_id?: number;

  message: string;

}

export interface ChatResponse {

  claim_id: number;

  question: string;

  answer: string;

  created_at: string;

}

export interface ChatMessage {

  sender: 'user' | 'assistant';

  text: string;

  timestamp: Date;

}