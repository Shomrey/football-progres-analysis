import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ServerConnectionService {

  private url: string = 'http://192.168.0.105:5000/';
  private obj: any;

  constructor(private http: HttpClient) { }



  getPerspectivePlayers(position: string, year: number, age: number): Observable<[]>{
    let specUrl = '/perspective/'+position;
    if(year !== 0)
    {
      specUrl += ('?season='+year);
    }    
    if(year !== 0)
    {
      specUrl += ('?max_age='+age);
    }
    return this.http.get<[]>(this.url+specUrl);
  }
}
