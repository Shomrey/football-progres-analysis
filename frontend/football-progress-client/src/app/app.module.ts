import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LayoutComponent } from './component/layout/layout.component';
import { PerspectivePlayersComponent } from './component/perspective-players/perspective-players.component';
import { WelcomeComponent } from './component/welcome/welcome.component';
import { HeadToHeadComponent } from './component/head-to-head/head-to-head.component';
import { FormsModule } from '@angular/forms';
import { ClosestPlayersComponent } from './component/closest-players/closest-players.component';
import { PlayerDetailsComponent } from './component/player-details/player-details.component';
import { PlayerDetailsWrapperComponent } from './component/player-details-wrapper/player-details-wrapper.component';


@NgModule({
  declarations: [
    AppComponent,
    LayoutComponent,
    PerspectivePlayersComponent,
    WelcomeComponent,
    HeadToHeadComponent,
    ClosestPlayersComponent,
    PlayerDetailsComponent,
    PlayerDetailsWrapperComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
