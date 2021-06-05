import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, retry, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ServerConnectionService {

  private url: string = 'http://127.0.0.1:5000/';

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

  getHeadToHead(firstName: string, firstSurname: string, firstSeason: number, secondName: string, secondSurname: string, secondSeason: number): Observable<any>
  {
    console.log(firstSeason)
    let specUrl = `player/compare?first1=${firstName}&second1=${firstSurname}&first2=${secondName}&second2=${secondSurname}&season1=${firstSeason}&season2=${secondSeason}`;
    return this.http.get<[]>(this.url+specUrl).pipe(tap(console.log));
  }
}
