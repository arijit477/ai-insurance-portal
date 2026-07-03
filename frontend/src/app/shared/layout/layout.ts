import { Component } from '@angular/core';
import {Sidebar} from '../sidebar/sidebar';
import {Navbar} from '../navbar/navbar';
import {RouterOutlet} from '@angular/router';
import { ChatComponent } from '../../features/chat/chat/chat';

@Component({
  selector: 'app-layout',
  imports: [Sidebar, Navbar, RouterOutlet, ChatComponent],
  templateUrl: './layout.html',
  styleUrl: './layout.css',
})
export class Layout {}
