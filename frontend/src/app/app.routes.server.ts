import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: '**',
    // Render on the client to avoid blank screens for parameterized routes (e.g. :id).
    renderMode: RenderMode.Client,
  },
];


