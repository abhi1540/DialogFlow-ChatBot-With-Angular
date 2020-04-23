import {AfterViewInit, Component, OnInit , ElementRef, ViewChild, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatBotService, Message } from './chatbot.service'
import { Observable } from 'rxjs'

import { scan } from 'rxjs/operators';


const dialogflowURL = 'https://console.dialogflow.com/api-client/demo/embedded/40dafba4-c362-443e-8abf-9b97c9dbdc43';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
//   template:`
//   <style>
// minimize= {height:'1.5rem',position:'fixed',bottom:0,overflow:'hidden'}
//   maximize={height:'100vh'}

// </style>

//   `


})
export class ChatbotComponent implements OnInit  {

messages: Observable<Message[]>;
formvalue: string;
buttonValue: string;
@ViewChild('target') target: ElementRef;
@ViewChild('window_handler') window_handler: ElementRef;


  constructor(private chat: ChatBotService) { }

  ngOnInit() {
this.messages = this.chat.conversation.asObservable().pipe(
  scan((acc, val) => acc.concat(val))
);
  }
sendMessage(){
  this.chat.converse(this.formvalue)
  this.formvalue = ''
}



  toggle(button) {
    this.buttonValue = button.id;
    if(this.buttonValue == "minimise"){
      this.target.nativeElement.style.display = "none"
      this.window_handler.nativeElement.style.top = "90%"
    }
    else{
      this.target.nativeElement.style.display = "block"
      this.window_handler.nativeElement.style.top = "18%"
    }
  }


}
