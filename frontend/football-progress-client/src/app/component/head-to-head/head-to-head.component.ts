import { Component, OnInit } from '@angular/core';
import { ServerConnectionService } from 'src/app/service/server-connection.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-head-to-head',
  templateUrl: './head-to-head.component.html',
  styleUrls: ['./head-to-head.component.scss']
})
export class HeadToHeadComponent implements OnInit {

  firstPlayerFirstName: string = '';
  firstPlayerSurname: string = '';
  firstPlayerSeason: number | undefined;
  secondPlayerFirstName: string = '';
  secondPlayerSurname: string = '';
  secondPlayerSeason: number | undefined;

  firstPlayer: any | undefined = {};
  secondPlayer: any | undefined = {};
  pathToChart: string = '';//'assets/Bednarek_Kompany.png'; //'C:\\Users\\SSD2\\Desktop\\AGH\\Eksploracja danych\\Projekt\\dynamic_charts\\Bednarek_Kompany.png'; 
  playersLoaded: boolean = false;
  wrongData: boolean = false;
  constructor(private serverConnectionService: ServerConnectionService, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  compare(): void {
    this.serverConnectionService.getHeadToHead(this.firstPlayerFirstName, this.firstPlayerSurname, this.firstPlayerSeason, this.secondPlayerFirstName, this.secondPlayerSurname, this.secondPlayerSeason)
    .subscribe(obj => {
      this.firstPlayer = obj.player_data_1[0];
      this.secondPlayer = obj.player_data_2[0];
      this.pathToChart = 'assets/' + obj.pathToChart;
      this.playersLoaded = true;
      this.wrongData = false;
      console.log(this.firstPlayer);
      console.log(this.secondPlayer);
      if(this.firstPlayer === undefined || this.secondPlayer === undefined)
      {
        this.playersLoaded = false;
        this.wrongData = true;
      }
    },
    err => {
      this.playersLoaded = false;
      this.wrongData = true;
    });
  }

  buttonEnabled(): boolean {
    return this.firstPlayerFirstName.length > 0 && this.firstPlayerSurname.length > 0 && this.firstPlayerSeason !== undefined && this.secondPlayerSeason !== undefined && this.secondPlayerSurname.length > 0 && this.secondPlayerFirstName.length > 0;
  }

  /*getSafeResource() {
    this.sanitizer.bypassSecurityTrustResourceUrl(this.pathToChart);
  }*/


}
