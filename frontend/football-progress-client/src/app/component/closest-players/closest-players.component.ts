import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { ServerConnectionService } from 'src/app/service/server-connection.service';

@Component({
  selector: 'app-closest-players',
  templateUrl: './closest-players.component.html',
  styleUrls: ['./closest-players.component.scss']
})
export class ClosestPlayersComponent implements OnInit {

  players: object[] = [];
  playerIdx = -1;
  neighSeason: number | undefined;
  year: number | undefined;
  firstName: string = '';
  surname: string = '';
  predictedValue: number;
  constructor(private serverConnectionService: ServerConnectionService) { }

  ngOnInit(): void {
  }

  setPlayerIdx(idx): void {
    this.playerIdx = idx;
  }

  showPlayer(): boolean {
    return this.playerIdx === -1;
  }

  getClosestPlayers() { 
    //this.subscribtion?.unsubscribe();  
    this.serverConnectionService.getClosestPlayers(this.firstName, this.surname, this.year, this.neighSeason).subscribe(result => 
      {
        this.players = result['players'];
        this.predictedValue = result.predicted_value;
        console.log(this.players);
      });
  }

  buttonEnabled(): boolean {
    return this.firstName.length > 0 && this.surname.length > 0 && this.year !== undefined && this.neighSeason !== undefined;
  }

}
