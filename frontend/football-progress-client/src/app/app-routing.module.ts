import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClosestPlayersComponent } from './component/closest-players/closest-players.component';
import { HeadToHeadComponent } from './component/head-to-head/head-to-head.component';
import { PerspectivePlayersComponent } from './component/perspective-players/perspective-players.component';
import { PlayerDetailsWrapperComponent } from './component/player-details-wrapper/player-details-wrapper.component';
import { WelcomeComponent } from './component/welcome/welcome.component';

const routes: Routes = [
  {path: '', redirectTo: 'perspective-players', pathMatch: 'full'},
  {path: 'perspective-players', component: PerspectivePlayersComponent},
  {path: 'head-to-head', component: HeadToHeadComponent},
  {path: 'closest-players', component: ClosestPlayersComponent},
  {path: 'player-details', component: PlayerDetailsWrapperComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
