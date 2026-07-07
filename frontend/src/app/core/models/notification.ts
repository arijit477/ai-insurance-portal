export interface Notification {
  id: number;
  user_id: number;
  claim_id: number | null;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}
