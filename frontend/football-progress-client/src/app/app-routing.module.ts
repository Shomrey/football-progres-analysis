import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HeadToHeadComponent } from './component/head-to-head/head-to-head.component';
import { PerspectivePlayersComponent } from './component/perspective-players/perspective-players.component';
import { WelcomeComponent } from './component/welcome/welcome.component';

const routes: Routes = [
  {path: '', component: WelcomeComponent},
  {path: 'perspective-players', component: PerspectivePlayersComponent},
  {path: 'head-to-head', component: HeadToHeadComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
