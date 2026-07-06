import {
  Component,
  inject,
  OnInit,
  ViewChild,
  ElementRef,
  AfterViewChecked,
  OnDestroy,
  signal,
  computed,
} from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';

import { ChatService } from '../../../core/services/chat.service';
import { ChatMessage } from '../../../core/models/chat';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatIconModule, MatChipsModule, DatePipe],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class ChatComponent implements OnInit, AfterViewChecked, OnDestroy {
  private chatService = inject(ChatService);
  private router = inject(Router);
  private sanitizer = inject(DomSanitizer);

  opened = signal(false);
  loading = signal(false);
  message = signal('');
  claimId = signal<number | null>(null);

  /** Index of the message being typed out (-1 = none) */
  typingIndex = signal(-1);

  messages = signal<ChatMessage[]>([]);

  private typewriterTimer: ReturnType<typeof setTimeout> | null = null;
  /** Stores the full text so we can skip the animation if needed */
  private fullTypewriterText = '';

  @ViewChild('messagesContainer')
  messagesContainer!: ElementRef<HTMLDivElement>;

  suggestions = computed(() => {
    const cid = this.claimId();
    if (cid !== null) {
      return ['Summarize this claim', 'Explain fraud score', 'Show detected damages', 'Missing documents'];
    }
    return ['How do I file a claim?', 'What does my policy cover?', 'How is fraud detected?', 'Check claim status'];
  });

  welcomeText = computed(() => {
    const cid = this.claimId();
    return cid !== null
      ? `Hello 👋 I'm AuraGuard AI. Ask me anything about Claim #${cid}.`
      : `Hello 👋 I'm AuraGuard AI. How can I help you today?`;
  });

  isTyping = computed(() => this.typingIndex() !== -1);

  ngOnInit(): void {
    this.extractClaimId(this.router.url);
    this.router.events
      .pipe(filter((e) => e instanceof NavigationEnd))
      .subscribe((e: NavigationEnd) => this.extractClaimId(e.urlAfterRedirects));
  }

  ngOnDestroy(): void {
    if (this.typewriterTimer) clearTimeout(this.typewriterTimer);
  }

  private extractClaimId(url: string): void {
    const match = url.match(/(?:claims|ai-report)\/(\d+)/);
    const newId = match ? Number(match[1]) : null;
    if (newId !== this.claimId()) {
      this.claimId.set(newId);
      this.skipTypewriter(); // complete any animation before resetting
      this.messages.set([{ sender: 'assistant', text: this.welcomeText(), timestamp: new Date() }]);
    }
  }

  private shouldScroll = false;

  ngAfterViewChecked(): void {
    if (this.shouldScroll && this.messagesContainer) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  scrollToBottom(): void {
    if (this.messagesContainer) {
      const el = this.messagesContainer.nativeElement;
      el.scrollTop = el.scrollHeight;
    }
  }

  toggle(): void {
    const isOpened = !this.opened();
    this.opened.set(isOpened);
    if (!isOpened) {
      // Window closing — finish any running animation instantly
      // so the user sees the complete message when they reopen
      this.skipTypewriter();
    } else {
      // Window opening — scroll to bottom to show latest message
      this.shouldScroll = true;
    }
  }

  /** Cancels the typewriter timer and immediately shows the full response */
  private skipTypewriter(): void {
    if (this.typewriterTimer) {
      clearTimeout(this.typewriterTimer);
      this.typewriterTimer = null;
    }
    const tIdx = this.typingIndex();
    if (tIdx !== -1 && this.fullTypewriterText) {
      const currentMsgs = [...this.messages()];
      currentMsgs[tIdx] = {
        ...currentMsgs[tIdx],
        text: this.fullTypewriterText,
      };
      this.messages.set(currentMsgs);
      this.typingIndex.set(-1);
      this.fullTypewriterText = '';
    }
  }

  send(): void {
    const msgVal = this.message().trim();
    if (!msgVal || this.loading()) return;

    this.message.set('');
    this.loading.set(true);
    this.shouldScroll = true;

    this.messages.update((msgs) => [...msgs, { sender: 'user', text: msgVal, timestamp: new Date() }]);

    this.chatService.ask({
      claim_id: this.claimId() ?? undefined,
      message: msgVal,
    }).subscribe({
      next: (response) => {
        this.loading.set(false);
        this.runTypewriter(response.answer);
      },
      error: () => {
        this.loading.set(false);
        this.messages.update((msgs) => [
          ...msgs,
          {
            sender: 'assistant',
            text: '⚠️ Sorry, something went wrong. Please try again.',
            timestamp: new Date(),
          }
        ]);
        this.shouldScroll = true;
      },
    });
  }

  /** Animates the AI response word by word */
  private runTypewriter(fullText: string): void {
    this.fullTypewriterText = fullText; // store for skip
    this.messages.update((msgs) => [...msgs, { sender: 'assistant', text: '', timestamp: new Date() }]);
    const index = this.messages().length - 1;
    this.typingIndex.set(index);
    this.shouldScroll = true;

    const words = fullText.match(/\S+\s*/g) ?? [fullText];
    let wordPos = 0;

    const type = () => {
      if (wordPos < words.length) {
        const currentMsgs = [...this.messages()];
        currentMsgs[index] = {
          ...currentMsgs[index],
          text: words.slice(0, wordPos + 1).join(''),
        };
        this.messages.set(currentMsgs);
        wordPos++;
        this.shouldScroll = true;
        this.typewriterTimer = setTimeout(type, 30);
      } else {
        this.typingIndex.set(-1);
        this.typewriterTimer = null;
        this.fullTypewriterText = '';
      }
    };

    type();
  }

  formatMessage(text: string): SafeHtml {
    if (!text) return '';
    
    // Escaping HTML characters first to prevent XSS
    let html = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Code blocks: ```code``` -> <pre><code>$1</code></pre>
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // Inline code: `code` -> <code>$1</code>
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold text: **text** -> <strong>$1</strong>
    html = html.replace(/\*\*([\s\S]*?)\*\*/g, '<strong>$1</strong>');

    // Bullet points:
    // Any line starting with "* " or "- " or "• " -> formatted as list item
    const lines = html.split('\n');
    let inList = false;
    const formattedLines = lines.map(line => {
      const match = line.match(/^(\s*)([*•-]\s+)(.+)$/);
      if (match) {
        let prefix = '';
        if (!inList) {
          inList = true;
          prefix = '<ul class="chat-list">';
        }
        return prefix + `<li>${match[3]}</li>`;
      } else {
        let prefix = '';
        if (inList) {
          inList = false;
          prefix = '</ul>';
        }
        return prefix + line;
      }
    });
    if (inList) {
      formattedLines.push('</ul>');
    }
    html = formattedLines.join('\n');

    // Convert newlines to <br/>
    html = html.replace(/\n/g, '<br/>');

    // Clean up empty double <br/> around list tags
    html = html.replace(/<\/ul><br\/>/g, '</ul>');
    html = html.replace(/<ul class="chat-list"><br\/>/g, '<ul class="chat-list">');
    html = html.replace(/<\/li><br\/>/g, '</li>');

    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  askSuggestion(question: string): void {
    this.message.set(question);
    this.send();
  }
}
