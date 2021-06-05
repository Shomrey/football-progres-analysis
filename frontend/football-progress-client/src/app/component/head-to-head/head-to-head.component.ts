import { Component, OnInit } from '@angular/core';
import { ServerConnectionService } from 'src/app/service/server-connection.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-head-to-head',
  templateUrl: './head-to-head.component.html',
  styleUrls: ['./head-to-head.component.scss']
})
export class HeadToHeadComponent implements OnInit {

  firstPlayerFirstName: string = 'Jan';
  firstPlayerSurname: string = 'Bednarek';
  firstPlayerSeason: number = 2020;
  secondPlayerFirstName: string = 'Vincent';
  secondPlayerSurname: string = 'Kompany';
  secondPlayerSeason: number = 2018;

  firstPlayer: any = {};
  secondPlayer: any = {};
  pathToChart: string = 'assets/Bednarek_Kompany.png'; //'C:\\Users\\SSD2\\Desktop\\AGH\\Eksploracja danych\\Projekt\\dynamic_charts\\Bednarek_Kompany.png'; 
  playersLoaded: boolean = false;
  constructor(private serverConnectionService: ServerConnectionService, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  compare(): void {
    this.serverConnectionService.getHeadToHead(this.firstPlayerFirstName, this.firstPlayerSurname, this.firstPlayerSeason, this.secondPlayerFirstName, this.secondPlayerSurname, this.secondPlayerSeason)
    .subscribe(obj => {
      this.firstPlayer = obj.player_data_1[0];
      this.secondPlayer = obj.player_data_2[0];
      //this.pathToChart = obj.pathToChart;
      this.playersLoaded = true;
      console.log(this.firstPlayer);
      console.log(this.secondPlayer);
    });
  }

  /*getSafeResource() {
    this.sanitizer.bypassSecurityTrustResourceUrl(this.pathToChart);
  }*/


}
