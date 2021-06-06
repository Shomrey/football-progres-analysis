import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-player-details-wrapper',
  templateUrl: './player-details-wrapper.component.html',
  styleUrls: ['./player-details-wrapper.component.scss']
})
export class PlayerDetailsWrapperComponent implements OnInit {

  playerFirstName: string = '';
  playerSurname: string = '';
  playerSeason: number;

  playerLoaded: boolean = false;
  constructor() { }

  ngOnInit(): void {
  }

  search(): void {
    if(this.playerFirstName.length > 0 && this.playerSurname.length > 0 ) this.playerLoaded = true;
  }

  back(): void {
    this.playerLoaded = false;
  }


}
