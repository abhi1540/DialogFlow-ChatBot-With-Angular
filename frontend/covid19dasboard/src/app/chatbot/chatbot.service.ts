import { Injectable } from "@angular/core";
import { environment } from '../../environments/environment'
import { Observable } from 'rxjs'
import { BehaviorSubject } from 'rxjs'
import { HttpClient } from '@angular/common/http';
import { shareReplay, map } from 'rxjs/operators';


import {ApiAiClient} from 'api-ai-javascript/es6/ApiAiClient';

export class Message{
  constructor(public content: string, public sentBy: string){}
}



@Injectable()
export class ChatBotService{

readonly token = environment.dialogflow.key;
readonly client = new ApiAiClient({accessToken: this.token})
conversation = new BehaviorSubject<Message[]>([]);

  constructor(private httpClient: HttpClient){}

  update(msg: Message){
this.conversation.next([msg])
  }

converse(msg: string){
const userMessage = new Message(msg, 'user');
this.update(userMessage)

return this.client.textRequest(msg)
                  .then(res => {
                      console.log(res);
                      const speech = res.result.fulfillment.speech;
                      const botmessage = new Message(speech, 'bot')
                      this.update(botmessage);
                    });
                    // if(res.result.fulfillment.messages[1].speech){
                    //   const speech = res.result.fulfillment.messages[1].speech;
                    //   const botmessage = new Message(speech, 'bot')
                    //   this.update(botmessage);
                    // }
                    // else{
                    //   const speech = res.result.fulfillment.messages[0].speech;
                    //   const botmessage = new Message(speech, 'bot')
                    //   this.update(botmessage);
                    // }
                    //console.log(speech)

                    // if ((res.result.action == "userdetl") &&
                    // (res.result.parameters.email != "") &&
                    // (res.result.parameters.phone_num != "") &&
                    // (res.result.parameters.zip_code != "")) {
                    //   this.httpClient.post("https://f354d812.ngrok.io/api/test", res).subscribe((data: any)=>{
                    //     console.log(data)
                    //     console.log(data.result.fulfillment.messages.speech)

                    //   this.data = data.result.fulfillment.speech;;
                    //     console.log(this.data)
                    //   })
                    //   const botmessage = new Message("this is test resp", 'bot')
                    //   this.update(botmessage);
                    // }
                    // else{
                    //   console.log(res)
                    //   const speech = res.result.fulfillment.speech;

                    //   const botmessage = new Message(speech, 'bot')
                    //   this.update(botmessage);
                    // }








}




}


