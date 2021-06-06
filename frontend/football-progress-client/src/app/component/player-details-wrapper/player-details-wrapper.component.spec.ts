import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerDetailsWrapperComponent } from './player-details-wrapper.component';

describe('PlayerDetailsWrapperComponent', () => {
  let component: PlayerDetailsWrapperComponent;
  let fixture: ComponentFixture<PlayerDetailsWrapperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PlayerDetailsWrapperComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayerDetailsWrapperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
