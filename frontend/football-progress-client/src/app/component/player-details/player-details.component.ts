import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { ServerConnectionService } from 'src/app/service/server-connection.service';

@Component({
  selector: 'app-player-details',
  templateUrl: './player-details.component.html',
  styleUrls: ['./player-details.component.scss']
})
export class PlayerDetailsComponent implements OnInit {

  @Input() firstName: string = ''; 
  @Input() surname: string = '';
  @Input() year: number;

  @Output() goBack = new EventEmitter<void>();

  playerDataList: any[] = [];
  pathToChart: string = '';
  keyList: string[] = [];
  constructor(private serverConnectionService: ServerConnectionService) { }

  ngOnInit(): void {
    this.serverConnectionService.getPlayer(this.firstName, this.surname, this.year).subscribe(
      data => {
        this.playerDataList = data.player_data;
        this.pathToChart = 'assets/' + data.pathToChart;
        this.keyList = Object.getOwnPropertyNames(this.playerDataList[0]);
        console.log(this.playerDataList);
      }
    )
  }

  back(): void {
    this.goBack.emit();
  }

}
