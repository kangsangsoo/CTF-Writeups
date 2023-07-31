mod entrypoint;

use solana_program::{
    account_info::AccountInfo,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
};
use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::account_info::next_account_info;
use solana_program::program::{invoke, invoke_signed};
use solana_program::{
    instruction::{AccountMeta, Instruction},
};




#[derive(BorshDeserialize, BorshSerialize)]
pub enum TribunalInstruction {
    Initialize { config_bump: u8, vault_bump: u8 },
    Propose { proposal_id: u8, proposal_bump: u8 },
    Vote { proposal_id: u8, amount: u64 },
    Withdraw { amount: u64 },
}

#[repr(u8)]
#[derive(BorshSerialize, BorshDeserialize, PartialEq)]
pub enum Types {
    Config,
    Proposal,
    Vault,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Config {
    pub discriminator: Types,
    pub admin: Pubkey,
    pub total_balance: u64,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Proposal {
    pub discriminator: Types,
    pub creator: Pubkey,
    pub balance: u64,
    pub proposal_id: u8,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Vault {
    pub discriminator: Types,
}

pub const CONFIG_SIZE: usize = std::mem::size_of::<Config>();
pub const PROPOSAL_SIZE: usize = std::mem::size_of::<Proposal>();
pub const VAULT_SIZE: usize = std::mem::size_of::<Vault>();


pub fn find_my_program_address(seeds: &[&[u8]], program_id: &Pubkey) -> Option<(Pubkey, u8)> {
    {
        let mut bump_seed = [0];
        for _ in 0..std::u8::MAX {
            {
                let mut seeds_with_bump = seeds.to_vec();
                seeds_with_bump.push(&bump_seed);
                match Pubkey::create_program_address(&seeds_with_bump, program_id) {
                    Ok(address) => return Some((address, bump_seed[0])),
                    Err(_) => (),
                }
            }
            bump_seed[0] += 1;
        }
        None
    }
}