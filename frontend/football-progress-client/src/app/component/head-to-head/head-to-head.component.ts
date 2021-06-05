import { Component, OnInit } from '@angular/core';
import { ServerConnectionService } from 'src/app/service/server-connection.service';

@Component({
  selector: 'app-head-to-head',
  templateUrl: './head-to-head.component.html',
  styleUrls: ['./head-to-head.component.scss']
})
export class HeadToHeadComponent implements OnInit {

  firstPlayerFirstName: string = '';
  firstPlayerSurname: string = '';
  firstPlayerSeason: number;
  secondPlayerFirstName: string = '';
  secondPlayerSurname: string = '';
  secondPlayerSeason: number;

  firstPlayer: any = {};
  secondPlayer: any = {};
  pathToChart: string = '';
  constructor(private serverConnectionService: ServerConnectionService) { }

  ngOnInit(): void {
  }

  compare(): void {
    this.serverConnectionService.getHeadToHead(this.firstPlayerFirstName, this.firstPlayerSurname, this.firstPlayerSeason, this.secondPlayerFirstName, this.secondPlayerSurname, this.secondPlayerSeason)
    .subscribe(obj => {
      this.firstPlayer = obj.player_data_1;
      this.secondPlayer = obj.player_data_2;
      this.pathToChart = obj.pathToChart;
    });
  }


}
