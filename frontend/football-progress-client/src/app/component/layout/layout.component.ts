import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServerConnectionService } from 'src/app/service/server-connection.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {

  constructor(private router: Router) { }


  ngOnInit(): void {
  }

  navigatePerspectivePlayers(): void {
    this.router.navigateByUrl('/perspective-players')
  }

  navigateHeadToHead(): void {
    this.router.navigateByUrl('/head-to-head')
  }

  navigateClosest(): void {
    //this.router.navigateByUrl('/head-to-head')
  }

}
