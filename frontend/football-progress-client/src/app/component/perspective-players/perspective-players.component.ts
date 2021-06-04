import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { ServerConnectionService } from 'src/app/service/server-connection.service';

@Component({
  selector: 'app-perspective-players',
  templateUrl: './perspective-players.component.html',
  styleUrls: ['./perspective-players.component.scss']
})
export class PerspectivePlayersComponent implements OnInit {

  private subscribtion: Subscription;
  private availablePositions: string[] = ['forwards', 'wingers', 'midfielders'];
  private position: string;
  players: object[] = [];
  playerIdx = -1;
  age: number = 0;
  year: number = 0;
  constructor(private serverConnectionService: ServerConnectionService) { }

  ngOnInit(): void {
    this.position = this.availablePositions[0];
  }

  setPlayerIdx(idx): void {
    this.playerIdx = idx;
  }

  showPlayer(): boolean {
    return this.playerIdx === -1;
  }

  getPerspectivePlayers() { 
    console.log(this.position);
    this.subscribtion?.unsubscribe();  
    this.subscribtion = this.serverConnectionService.getPerspectivePlayers(this.position, this.year, this.age).subscribe(result => this.players = result['players']);
    this.log(this.players);
  }

  log(toLog: any)
  {
    console.log(toLog);
  }

  selectChangeHandler (event: any) {
    //update the ui
    this.position = event.target.value;
  }

}
