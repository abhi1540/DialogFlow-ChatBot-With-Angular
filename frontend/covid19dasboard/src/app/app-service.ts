import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { shareReplay, map } from 'rxjs/operators';
import { delay } from "rxjs/operators";

const CACHE_SIZE = 1;

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private cache$: Observable<any>;

  get data() {
    if (!this.cache$) {
      this.cache$ = this.getData().pipe(
        shareReplay(CACHE_SIZE)
      );
      console.log(this.cache$)
    }

    return this.cache$;
  }
  constructor(private httpClient: HttpClient) { }

  public getData(){
    return this.httpClient.get("https://f354d812.ngrok.io/api/covidapicountrywise/").pipe(
      map(data => data),
    );
  }

}


