import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, retry, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ServerConnectionService {

  private url: string = 'http://192.168.0.105:5000/';

  constructor(private http: HttpClient) { }

  getPerspectivePlayers(position: string, year: number, age: number): Observable<[]>{
    let specUrl = '/perspective/'+position;
    if(year !== 0)
    {
      specUrl += ('?season='+year);
    }    
    if(age !== 0)
    {
      specUrl += ('&max_age='+age);
    }
    console.log(this.url+specUrl);
    return this.http.get<[]>(this.url+specUrl);
  }

  getHeadToHead(firstName: string, firstSurname: string, firstSeason: number, secondName: string, secondSurname: string, secondSeason: number): Observable<any>
  {
    console.log(firstSeason)
    let specUrl = `player/compare?first1=${firstName}&second1=${firstSurname}&first2=${secondName}&second2=${secondSurname}&season1=${firstSeason}&season2=${secondSeason}`;
    return this.http.get<[]>(this.url+specUrl);
  }

  getClosestPlayers(firstName: string, surname: string, year: number, neighSeason: number): Observable<any>
  {
    let specUrl = `closest?first=${firstName}&second=${surname}&season=${year}&neighseason=${neighSeason}`
    return this.http.get<[]>(this.url+specUrl);
  }

  getPlayer(firstName: string, surname: string, year: number): Observable<any>
  {
    let yearString = year > 0 ? `&year=${year}` : ''
    let specUrl = `player?first=${firstName}&second=${surname}${yearString}`;
    return this.http.get(this.url+specUrl);
  }
}
