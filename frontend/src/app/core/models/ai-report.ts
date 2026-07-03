export interface AIReport {

  id: number;

  claim_id: number;

  ocr_text: string | null;

  ocr_result: Record<string, any> | null;

  extracted_data: Record<string, any> | null;

  claim_verification: Record<string, any> | null;

  claim_summary: string | null;

  damage_analysis: Record<string, any> | null;

  fraud_analysis: Record<string, any> | null;

  final_decision: Record<string, any> | null;

  fraud_score: number;

  ai_completed: boolean;

  processing_time: number;

  model_name: string | null;

  created_at: string;

  updated_at: string;

}